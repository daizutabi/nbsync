from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import nbformat
from nbstore.markdown import CodeBlock, Image
from nbstore.notebook import get_language, get_mime_content, get_source

import nbsync.markdown
from nbsync import logger
from nbsync.cell import Cell
from nbsync.markdown import is_truelike
from nbsync.notebook import Notebook

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
                update_notebooks(elem, notebooks, self.store)

        for url, notebook in notebooks.items():
            if url not in self.notebooks or not self.notebooks[url].equals(notebook):
                self.notebooks[url] = notebook

    def execute(self) -> None:
        for url, notebook in self.notebooks.items():
            if not notebook.execution_needed:
                continue

            path = ".md" if url == ".md" else self.store.find_path(url)
            logger.info(f"Executing notebook: {path}")
            if elapsed := notebook.execute():
                logger.info(f"{Path(path).name!r} executed in {elapsed:.2f} seconds")

    def convert(self, text: str) -> Iterator[str | Cell]:
        elems = list(self.parse(text))
        self.execute()

        for elem in elems:
            if isinstance(elem, str):
                yield elem

            elif cell := convert(elem, self.notebooks):
                yield cell


def update_notebooks(
    elem: Image | CodeBlock,
    notebooks: dict[str, Notebook],
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


def convert(
    elem: Image | CodeBlock,
    notebooks: dict[str, Notebook],
) -> str | Cell:
    if elem.identifier not in [".", "_"] or "source" in elem.attributes:
        if isinstance(elem, Image):
            if elem.url not in notebooks:
                logger.warning(f"Notebook not found: {elem.url}")
                return ""

            nb = notebooks[elem.url].nb
            return convert_image(elem, nb)

        return convert_code_block(elem)

    return ""


def convert_image(image: Image, nb: NotebookNode) -> Cell:
    try:
        image.source = get_source(nb, image.identifier)
        mime_content = get_mime_content(nb, image.identifier)
    except ValueError:
        cell = f"{image.url}#{image.identifier}"
        logger.warning(f"Error reading cell: {cell!r}")
        image.source = ""
        mime_content = ("", "")

    return Cell(image, get_language(nb), *mime_content)


def convert_code_block(code_block: CodeBlock) -> str:
    source = code_block.attributes.pop("source", None)
    if not is_truelike(source):
        return ""

    lines = code_block.text.splitlines()
    if lines:
        pattern = f"\\S+#{code_block.identifier}"
        lines[0] = re.sub(pattern, "", lines[0])
        pattern = r"source=[^\s}]+"
        lines[0] = re.sub(pattern, "", lines[0])

    return "\n".join(lines)
