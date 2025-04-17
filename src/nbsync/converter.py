from __future__ import annotations

from typing import TYPE_CHECKING

from .figure import Figure
from .logger import logger
from .markdown import Image, iter_elements

if TYPE_CHECKING:
    from collections.abc import Iterator

    from nbstore import Store

    from .markdown import Element


def convert(markdown: str, store: Store) -> Iterator[str | Figure]:
    for elem in iter_elements(markdown):
        if isinstance(elem, str):
            yield elem
        else:
            yield from convert_element(elem, store)


def convert_element(elem: Element, store: Store) -> Iterator[str | Figure]:
    if isinstance(elem, Image):
        yield from convert_image(elem, store)
    else:
        yield elem.text


def is_truelike(value: str | None) -> bool:
    return value is not None and value.lower() in ("yes", "true", "1")


def convert_image(image: Image, store: Store) -> Iterator[str | Figure]:
    if image.url and not any(image.url.endswith(x) for x in (".ipynb", ".py")):
        yield image.text
        return

    nb = store.get_notebook(image.url)

    exec_ = image.attributes.pop("exec", None)
    if is_truelike(exec_) and store.needs_execution(image.url):
        logger.info(f"Executing notebook: {nb.path}")
        nb.execute()

    if image.identifier == "_":
        return

    source = image.attributes.pop("source", None)
    if has_source := (is_truelike(source) or source == "only"):
        yield from get_source(image, nb)

    if source == "only":
        return

    if mime_content := nb.get_mime_content(image.identifier):
        fig = Figure.from_element(image)
        yield fig.convert(*mime_content)

    elif not has_source:
        yield from get_source(image, nb)


def get_source(image: Image, nb: Notebook) -> Iterator[str]:
    if source := nb.get_source(image.identifier):
        language = "." + nb.get_language()
        attr = " ".join([language, *image.iter_parts()])
        yield f"```{{{attr}}}\n{source}\n```\n\n"
