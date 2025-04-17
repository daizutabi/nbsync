from __future__ import annotations

from typing import TYPE_CHECKING

import nbstore.notebook

if TYPE_CHECKING:
    from nbformat import NotebookNode


class Notebook:
    nb: NotebookNode
    execution_needed: bool

    def __init__(self, nb: NotebookNode) -> None:
        self.nb = nb
        self.execution_needed = False

    def set_execution_needed(self) -> None:
        self.execution_needed = True

    def add_cell(self, identifier: str, source: str) -> None:
        cell = nbstore.notebook.new_code_cell(identifier, source)
        self.nb.cells.append(cell)
        self.set_execution_needed()

    def equals(self, other: Notebook) -> bool:
        return nbstore.notebook.equals(self.nb, other.nb)

    def execute(self) -> None:
        nbstore.notebook.execute(self.nb)
        self.execution_needed = False
