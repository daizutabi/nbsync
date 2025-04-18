import nbformat
import nbstore.notebook

from nbsync.notebook import Notebook


def test_notebook():
    nb = nbformat.v4.new_notebook()
    notebook = Notebook(nb)
    assert notebook.execution_needed is False


def test_set_execution_needed():
    nb = nbformat.v4.new_notebook()
    notebook = Notebook(nb)
    notebook.set_execution_needed()
    assert notebook.execution_needed is True


def test_add_cell():
    nb = nbformat.v4.new_notebook()
    notebook = Notebook(nb)
    notebook.add_cell("id", "print('Hello, world!')")
    assert not nb.cells
    assert id(nb) != id(notebook.nb)
    nb = notebook.nb
    assert nbstore.notebook.get_source(nb, "id") == "print('Hello, world!')"
    assert notebook.execution_needed is True
    notebook.add_cell("id2", "1")
    assert id(nb) == id(notebook.nb)


def test_equals():
    nb1 = nbformat.v4.new_notebook()
    nb2 = nbformat.v4.new_notebook()
    notebook1 = Notebook(nb1)
    notebook2 = Notebook(nb2)
    assert notebook1.equals(notebook2) is True
    notebook1.add_cell("id", "print('Hello, world!')")
    assert notebook1.equals(notebook2) is False


def test_execute():
    nb = nbformat.v4.new_notebook()
    notebook = Notebook(nb)
    notebook.add_cell("id", "print(1+1)")
    notebook.execute()
    assert nbstore.notebook.get_stream(notebook.nb, "id") == "2\n"
    assert notebook.execution_needed is False
