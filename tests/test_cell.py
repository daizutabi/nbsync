import nbformat
import nbstore.notebook
import pytest
from nbstore import Store

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


@pytest.fixture(scope="module")
def store(nb, tmp_path_factory: pytest.TempPathFactory) -> Store:
    src_dir = tmp_path_factory.mktemp("src")
    nbformat.write(nb, src_dir.joinpath("a.ipynb"))
    return Store(src_dir)


@pytest.fixture(scope="module")
def sync(store):
    return Synchronizer(store)


@pytest.fixture(scope="module")
def convert(sync: Synchronizer):
    def convert(text: str) -> str:
        cell = next(sync.convert(text))
        assert isinstance(cell, Cell)
        return cell.convert()

    return convert


def test_text_plain(convert):
    assert convert("![a](a.ipynb){#id}") == "2"


def test_empty(convert):
    assert convert("![a](a.ipynb){#empty}") == ""


def test_image(convert):
    x = convert("![a](a.ipynb){#fig a b=c}")
    assert x.startswith("![a]")
    assert x.endswith(".png){#fig a b=c}")


def test_func(convert):
    x = convert("![a](a.ipynb){#func a=b c}")
    assert x == "```python c a=b\ndef f():\n    pass\n```"


@pytest.mark.parametrize("kind", ["above", "on", "1"])
def test_above(convert, kind):
    x = convert(f"![a](a.ipynb){{#fig source='{kind}' a b=c}}")
    assert x.startswith("```python\n")
    assert x.endswith(".png){#fig a b=c}")


def test_below(convert):
    x = convert("![a](a.ipynb){#fig source='below' a b=c}")
    assert x.startswith("![a](")
    assert x.endswith("[1])\n```")


def test_material_block(convert):
    x = convert("![a](a.ipynb){#fig source='material-block' a b=c}")
    assert '<div class="result" markdown="1">![a]' in x


def test_tabbed_left(convert):
    x = convert("![a](a.ipynb){#fig source='tabbed-left' a b=c}")
    assert x.startswith('===! "Source"\n\n    ```python\n')
    assert '=== "Result"\n\n    ![a]' in x


def test_tabbed_left_title(convert):
    x = convert("![a](a.ipynb){#fig source='tabbed-left' tabs='a|b'}")
    assert x.startswith('===! "a"\n\n    ```python\n')
    assert '=== "b"\n\n    ![a]' in x


def test_tabbed_right_title(convert):
    x = convert("![a](a.ipynb){#fig source='tabbed-right' tabs='a|b'}")
    assert x.startswith('===! "a"\n\n    ![a]')
    assert '=== "b"\n\n    ```python\n' in x


def test_unknown(convert):
    x = convert("![a](a.ipynb){#id source='unknown' tabs='a|b'}")
    assert x == "2"
