from __future__ import annotations

import copy
import os
import time
from typing import TYPE_CHECKING

import nbstore.notebook

from nbsync import logger

if TYPE_CHECKING:
    from nbformat import NotebookNode

# DeprecationWarning: Jupyter is migrating its paths to use standard platformdirs
os.environ.setdefault("JUPYTER_PLATFORM_DIRS", "1")


class Notebook:
    nb: NotebookNode
    is_modified: bool
    execution_needed: bool

    def __init__(self, nb: NotebookNode) -> None:
        self.nb = nb
        self.is_modified = False
        self.execution_needed = False

    def set_execution_needed(self) -> None:
        self.execution_needed = True

    def add_cell(self, identifier: str, source: str) -> None:
        if not self.is_modified:
            self.nb = copy.deepcopy(self.nb)
            self.is_modified = True

        cell = nbstore.notebook.new_code_cell(identifier, source)
        self.nb.cells.append(cell)
        self.set_execution_needed()

    def equals(self, other: Notebook) -> bool:
        return nbstore.notebook.equals(self.nb, other.nb)

    def execute(self) -> float:
        try:
            start_time = time.perf_counter()
            nbstore.notebook.execute(self.nb)
            end_time = time.perf_counter()
            self.execution_needed = False
            return end_time - start_time
        except ModuleNotFoundError as e:  # no cov
            logger.warning(e.msg)
            return 0
