from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING, TypeAlias

import nbstore.markdown
from nbstore.markdown import CodeBlock, Image

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

Element: TypeAlias = str | CodeBlock | Image


def convert_code_block(code_block: CodeBlock) -> Iterator[Element]:
    for elem in _convert_code_block_tabbed(code_block):
        if isinstance(elem, CodeBlock):
            yield _convert_code_block_attrs(elem)
        else:
            yield elem


def _convert_code_block_tabbed(code_block: CodeBlock) -> Iterator[Element]:
    source = code_block.attributes.get("source", None)
    if source != "tabbed-nbsync":
        yield code_block
        return

    markdown = code_block.text.replace('source="tabbed-nbsync"', "")
    markdown = textwrap.indent(markdown, "    ")
    yield f'===! "Markdown"\n\n{markdown}\n\n'

    text = textwrap.indent(code_block.source, "    ")
    text = f'=== "Rendered"\n\n{text}'
    yield from nbstore.markdown.parse(text)


def _convert_code_block_attrs(code_block: CodeBlock) -> CodeBlock | Image:
    exec_ = code_block.attributes.get("exec", None)
    if exec_ != "1" or not code_block.classes:
        return code_block

    if code_block.classes[0] != "python":
        return code_block

    del code_block.attributes["exec"]
    return Image(
        code_block.indent,
        "",
        code_block.classes[1:],
        code_block.attributes,
        code_block.source,
        url=".md",
        indent=code_block.indent,
    )


def convert_image(image: Image, index: int | None = None) -> Iterator[Element]:
    if image.source:
        if not image.identifier and index is None:
            msg = "index is required when source is present and identifier is not set"
            raise ValueError(msg)

        image.identifier = image.identifier or f"image-nbsync-{index}"
        yield CodeBlock("", image.identifier, [], {}, image.source, image.url)
        yield image

    elif image.identifier:
        yield image

    else:
        yield image.text


SUPPORTED_EXTENSIONS = (".ipynb", ".md", ".py")


def set_url(elem: Image | CodeBlock, url: str) -> tuple[Element, str]:
    """Set the URL of the image or code block.

    If the URL is empty or ".", set the URL to the current URL.
    """
    if elem.url in ["", "."] and url:
        elem.url = url
        return elem, url

    if elem.url.endswith(SUPPORTED_EXTENSIONS):
        return elem, elem.url

    return elem.text, url


def resolve_urls(elems: Iterable[Element]) -> Iterator[Element]:
    """Parse the URL of the image or code block.

    If a code block has no URL, yield the text of the code block,
    which means that the code block is not processed further.
    """
    url = ""

    for elem in elems:
        if isinstance(elem, CodeBlock) and not elem.url:
            yield elem.text

        elif isinstance(elem, Image | CodeBlock):
            elem_, url = set_url(elem, url)
            yield elem_

        else:
            yield elem


def convert_code_blocks(elems: Iterable[Element]) -> Iterator[Element]:
    for elem in elems:
        if isinstance(elem, CodeBlock):
            yield from convert_code_block(elem)
        else:
            yield elem


def convert_images(elems: Iterable[Element]) -> Iterator[Element]:
    for index, elem in enumerate(elems):
        if isinstance(elem, Image):
            yield from convert_image(elem, index)
        else:
            yield elem


def parse(text: str) -> Iterator[Element]:
    elems = nbstore.markdown.parse(text)
    elems = convert_code_blocks(elems)
    elems = resolve_urls(elems)
    yield from convert_images(elems)


def is_truelike(value: str | None) -> bool:
    return value is not None and value.lower() in ("yes", "true", "1", "on")
