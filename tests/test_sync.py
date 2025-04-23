import nbformat
import nbstore.notebook
import pytest
from nbstore import Store
from nbstore.markdown import CodeBlock, Image

from nbsync.cell import Cell
from nbsync.sync import Synchronizer


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


def test_convert_image(nb):
    from nbsync.sync import convert_image

    image = Image("abc", "id", [], {}, "", "a.py")
    x = convert_image(image, nb)
    assert isinstance(x, Cell)
    assert x.image.source == "print(1+1)"
    assert x.content == "2\n"
    assert x.mime == "text/plain"


def test_convert_image_invalid(nb):
    from nbsync.sync import convert_image

    image = Image("abc", "invalid", [], {}, "", "a.py")
    x = convert_image(image, nb)
    assert isinstance(x, Cell)
    assert x.image.source == ""
    assert x.content == ""
    assert x.mime == ""


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
    update_notebooks(Image("abc", "id", [], {}, "", "a.ipynb"), notebooks, store)
    assert len(notebooks) == 1
    nb = notebooks["a.ipynb"].nb
    assert nbstore.notebook.get_source(nb, "id") == "print(1+1)"


def test_update_notebooks_exec(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    image = Image("abc", "id", [], {"exec": "1"}, "", "a.ipynb")
    update_notebooks(image, notebooks, store)
    assert len(notebooks) == 1
    assert notebooks["a.ipynb"].execution_needed


def test_update_notebooks_add_cell(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    code_block = CodeBlock("abc", "id2", [], {}, "123", "a.ipynb")
    update_notebooks(code_block, notebooks, store)
    assert len(notebooks) == 1
    notebook = notebooks["a.ipynb"]
    assert notebook.execution_needed
    assert len(notebook.nb.cells) == 2
    assert len(store.read("a.ipynb").cells) == 1


def test_update_notebooks_self(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    code_block = CodeBlock("abc", "id2", [], {}, "123", ".md")
    update_notebooks(code_block, notebooks, store)
    assert len(notebooks) == 1
    notebook = notebooks[".md"]
    assert len(notebook.nb.cells) == 1


def test_update_notebooks_error(store: Store):
    from nbsync.sync import Notebook, update_notebooks

    notebooks: dict[str, Notebook] = {}
    code_block = CodeBlock("abc", "id2", [], {}, "123", "invalid.md")
    update_notebooks(code_block, notebooks, store)
    assert len(notebooks) == 0


def test_convert_code_block_none():
    from nbsync.sync import convert_code_block

    code_block = CodeBlock("abc", "id2", [], {}, "123", "a.ipynb")
    assert convert_code_block(code_block) == ""


def test_convert_code_block_brace():
    from nbsync.sync import convert_code_block

    text = '  ```{.python a#id source="on"}\n  a\n  ```'
    code_block = CodeBlock(text, "id", [], {"source": "on"}, "", "")
    x = "  ```{.python  }\n  a\n  ```"
    assert convert_code_block(code_block) == x


def test_convert_code_block_space():
    from nbsync.sync import convert_code_block

    text = '  ```.python a#id source="on" abc\n  a\n  ```'
    code_block = CodeBlock(text, "id", [], {"source": "on"}, "", "")
    x = "  ```.python   abc\n  a\n  ```"
    assert convert_code_block(code_block) == x


@pytest.fixture
def sync(store: Store):
    return Synchronizer(store)


def test_sync_str(sync: Synchronizer):
    x = list(sync.convert("abc"))
    assert x[0] == "abc"


def test_sync_image(sync: Synchronizer):
    x = next(sync.convert('![](a.ipynb){#id exec="1"}'))
    assert isinstance(x, Cell)
    assert x.image.source == "print(1+1)"
    assert x.content == "2\n"
    assert x.mime == "text/plain"
    notebook = sync.notebooks["a.ipynb"]
    x = next(sync.convert('![](a.ipynb){#id exec="1"}'))
    assert isinstance(x, Cell)
    assert x.image.source == "print(1+1)"
    assert x.content == "2\n"
    assert notebook is sync.notebooks["a.ipynb"]
    assert notebook.nb is sync.notebooks["a.ipynb"].nb


def test_sync_code_block(sync: Synchronizer):
    x = next(sync.convert("```a b.md#c source=1\nc\n```"))
    assert isinstance(x, str)
    assert x == "```a  \nc\n```"


def test_sync_notebook_not_found():
    from nbsync.sync import convert

    image = Image("abc", "id", [], {}, "", "a.ipynb")
    assert convert(image, {}) == ""
