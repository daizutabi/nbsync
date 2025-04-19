from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import nbformat
import nbstore.notebook
from nbstore.markdown import CodeBlock, Image

import nbsync.markdown
from nbsync.figure import Figure
from nbsync.notebook import Notebook

from .logger import logger

if TYPE_CHECKING:
    from collections.abc import Iterator

    from nbformat import NotebookNode
    from nbstore import Store


@dataclass
class Synchronizer:
    store: Store
    notebooks: dict[str, Notebook] = field(default_factory=dict, init=False)

    def parse(self, text: str) -> Iterator[str | Image | CodeBlock]:
        notebooks: dict[str, Notebook] = {}

        for elem in nbsync.markdown.parse(text):
            yield elem

            if isinstance(elem, Image | CodeBlock):
                update_notebooks(notebooks, elem, self.store)

        for url, notebook in notebooks.items():
            if url not in self.notebooks or not self.notebooks[url].equals(notebook):
                self.notebooks[url] = notebook

    def execute(self) -> None:
        for url, notebook in self.notebooks.items():
            if not notebook.execution_needed:
                continue

            path = ".md" if url == ".md" else self.store.find_path(url)
            logger.info(f"Executing notebook: {path}")
            notebook.execute()

    def convert(self, text: str) -> Iterator[str | Figure]:
        elems = list(self.parse(text))
        self.execute()

        for elem in elems:
            if isinstance(elem, str):
                yield elem

            elif elem.identifier not in [".", "_"]:
                if isinstance(elem, Image):
                    nb = self.notebooks[elem.url].nb
                    yield from convert_image(elem, nb)
                else:
                    yield from convert_code_block(elem)


def update_notebooks(
    notebooks: dict[str, Notebook],
    elem: Image | CodeBlock,
    store: Store,
) -> None:
    url = elem.url

    if url not in notebooks:
        if url == ".md":
            notebooks[url] = Notebook(nbformat.v4.new_notebook())
        else:
            try:
                notebooks[url] = Notebook(store.read(url))
            except Exception:  # noqa: BLE001
                logger.warning(f"Error reading notebook: {url}")
                return

    notebook = notebooks[url]

    if is_truelike(elem.attributes.pop("exec", None)):
        notebook.set_execution_needed()

    if isinstance(elem, CodeBlock):
        source = textwrap.dedent(elem.source)
        notebook.add_cell(elem.identifier, source)


def is_truelike(value: str | None) -> bool:
    return value is not None and value.lower() in ("yes", "true", "1", "on")


def convert_image(image: Image, nb: NotebookNode) -> Iterator[str | Figure]:
    source = image.attributes.pop("source", None)
    if has_source := (is_truelike(source) or source == "only"):
        yield get_source_from_image(image, nb)

    if source == "only":
        return

    try:
        mime_content = nbstore.notebook.get_mime_content(nb, image.identifier)
    except ValueError:
        cell = f"{image.url}#{image.identifier}"
        logger.warning(f"Error reading cell: {cell!r}")
        return

    if mime_content:
        yield Figure(image, *mime_content).convert()

    elif not has_source:
        yield get_source_from_image(image, nb)


def get_source_from_image(image: Image, nb: NotebookNode) -> str:
    source = nbstore.notebook.get_source(nb, image.identifier)
    if not source:
        return ""

    language = nbstore.notebook.get_language(nb)
    attr = " ".join([language, *image.iter_parts()])
    return f"```{attr}\n{source}\n```"


def convert_code_block(code_block: CodeBlock) -> str:
    source = code_block.attributes.pop("source", None)
    if is_truelike(source):
        attr = " ".join(code_block.iter_parts())
        text = f"```{attr}\n{code_block.source}\n```"
        return textwrap.indent(text, code_block.indent)

    return ""
