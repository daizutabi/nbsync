from __future__ import annotations

from typing import TYPE_CHECKING

import nbstore.notebook

if TYPE_CHECKING:
    from nbformat import NotebookNode


class Notebook:
    nb: NotebookNode
    is_executed: bool
    is_modified: bool

    def __init__(self, nb: NotebookNode) -> None:
        self.nb = nb
        self.is_executed = False
        self.is_modified = False

    def add_cell(self, identifier: str, source: str) -> None:
        cell = nbstore.notebook.new_code_cell(identifier, source)
        self.nb.cells.append(cell)
        self.is_modified = True

    def equals(self, other: Notebook) -> bool:
        return nbstore.notebook.equals(self.nb, other.nb)
