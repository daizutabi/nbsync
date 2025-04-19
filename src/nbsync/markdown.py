from __future__ import annotations

import textwrap
import uuid
from typing import TYPE_CHECKING, TypeAlias

import nbstore.markdown
from nbstore.markdown import CodeBlock, Image

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

Element: TypeAlias = str | CodeBlock | Image


def convert_image(image: Image) -> Iterator[Element]:
    if image.source:
        image.identifier = image.identifier or str(uuid.uuid4())
        yield CodeBlock("", image.identifier, [], {}, image.source, image.url)
        yield image

    elif image.identifier:
        yield image

    else:
        yield image.text


def convert_code_block(code_block: CodeBlock) -> Iterator[Element]:
    source = code_block.attributes.get("source", None)
    if source != "tabbed-nbsync":
        yield code_block
        return

    markdown = code_block.text.replace('source="tabbed-nbsync"', "")
    markdown = textwrap.indent(markdown, "    ")
    yield f'=== "Markdown"\n\n{markdown}\n\n=== "HTML"\n\n'

    text = textwrap.indent(code_block.source, "    ")
    yield from nbstore.markdown.parse(text)


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


def parse_url(elems: Iterable[Element]) -> Iterator[Element]:
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


def parse_code_block(elems: Iterable[Element]) -> Iterator[Element]:
    for elem in elems:
        if isinstance(elem, CodeBlock):
            yield from convert_code_block(elem)
        else:
            yield elem


def parse_image(elems: Iterable[Element]) -> Iterator[Element]:
    for elem in elems:
        if isinstance(elem, Image):
            yield from convert_image(elem)
        else:
            yield elem


def parse(text: str) -> Iterator[Element]:
    elems = nbstore.markdown.parse(text)
    elems = parse_code_block(elems)
    elems = parse_url(elems)
    yield from parse_image(elems)
