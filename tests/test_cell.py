import nbformat
import nbstore.notebook
import pytest
from nbstore import Store
from nbstore.markdown import CodeBlock, Image


@pytest.fixture(scope="module")
def nb():
    nb = nbformat.v4.new_notebook()
    for source in [
        "# #id\nprint(1+1)",
        "# #empty\n",
        "# #fig\nimport matplotlib.pyplot as plt\nplt.plot([1])",
        "# #func\ndef f():\n    pass",
    ]:
        nb.cells.append(nbformat.v4.new_code_cell(source))
    nbstore.notebook.execute(nb)
    return nb


def test_get_source(nb):
    from nbsync.sync import get_source_from_image

    image = Image("abc", "id", [], {}, "", "a.py")
    assert get_source_from_image(image, nb) == "```{.python}\nprint(1+1)\n```\n\n"


def test_get_source_none(nb):
    from nbsync.sync import get_source_from_image

    image = Image("abc", "empty", [], {}, "", "a.py")
    assert get_source_from_image(image, nb) == ""


def test_convert_image(nb):
    from nbsync.cell import Cell
    from nbsync.sync import convert_image

    image = Image("abc", "id", [], {}, "", "a.py")
    x = list(convert_image(image, nb))
    assert len(x) == 1
    fig = x[0]
    assert isinstance(fig, Cell)
    assert fig.content == "2\n"
    assert fig.mime == "text/plain"
    assert fig.src == ""


def test_convert_image_source(nb):
    from nbsync.cell import Cell
    from nbsync.sync import convert_image

    image = Image("abc", "id", [], {"source": "1"}, "", "a.py")
    source = "```{.python}\nprint(1+1)\n```\n\n"
    x = list(convert_image(image, nb))
    assert len(x) == 2
    assert x[0] == source
    assert isinstance(x[1], Cell)


def test_convert_image_source_only(nb):
    from nbsync.sync import convert_image

    image = Image("abc", "id", [], {"source": "only"}, "", "a.py")
    x = "```{.python}\nprint(1+1)\n```\n\n"
    assert list(convert_image(image, nb)) == [x]


def test_convert_image_fallback(nb):
    from nbsync.sync import convert_image

    image = Image("abc", "func", [], {}, "", "a.py")
    x = "```{.python}\ndef f():\n    pass\n```\n\n"
    assert list(convert_image(image, nb)) == [x]


@pytest.fixture(scope="module")
def store(tmp_path_factory: pytest.TempPathFactory) -> Store:
    src_dir = tmp_path_factory.mktemp("src")
    nb = nbformat.v4.new_notebook()
    nb.cells.append(nbformat.v4.new_code_cell("# #id\nprint(1+1)"))
    nbformat.write(nb, src_dir.joinpath("a.ipynb"))
    return Store(src_dir)


def test_update_notebooks(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    update_notebooks(notebooks, Image("abc", "id", [], {}, "", "a.ipynb"), store)
    assert len(notebooks) == 1
    nb = notebooks["a.ipynb"].nb
    assert nbstore.notebook.get_source(nb, "id") == "print(1+1)"


def test_update_notebooks_exec(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    image = Image("abc", "id", [], {"exec": "1"}, "", "a.ipynb")
    update_notebooks(notebooks, image, store)
    assert len(notebooks) == 1
    assert notebooks["a.ipynb"].execution_needed


def test_update_notebooks_add_cell(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    code_block = CodeBlock("abc", "id2", [], {}, "123", "a.ipynb")
    update_notebooks(notebooks, code_block, store)
    assert len(notebooks) == 1
    notebook = notebooks["a.ipynb"]
    assert notebook.execution_needed
    assert len(notebook.nb.cells) == 2
    assert len(store.read("a.ipynb").cells) == 1


def test_update_notebooks_self(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    code_block = CodeBlock("abc", "id2", [], {}, "123", ".md")
    update_notebooks(notebooks, code_block, store)
    assert len(notebooks) == 1
    notebook = notebooks[".md"]
    assert len(notebook.nb.cells) == 1
