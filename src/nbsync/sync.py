from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from nbformat import NotebookNode
from nbstore import Store
from nbstore.markdown import CodeBlock, Image, iter_elements

if TYPE_CHECKING:
    from collections.abc import Iterable


class Synchronizer:
    store: Store
    notebooks: dict[str, NotebookNode]

    def __init__(self, src_dirs: str | Path | Iterable[str | Path]) -> None:
        self.store = Store(src_dirs)

    def parse(self, text: str) -> None:
        url = ""
        notebooks = {}
        elems = []

        for elem in iter_elements(text):
            if isinstance(elem, Image):