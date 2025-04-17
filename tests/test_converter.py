from nbstore.store import Store

from nbsync.converter import convert
from nbsync.figure import Figure


def test_convert_source(store: Store):
    markdown = "![a](matplotlib.ipynb){#matplotlib source=1}\n\na"
    it = convert(markdown, store)

    source = next(it)
    assert isinstance(source, str)
    assert source.startswith("```{.python}\n")

    image = next(it)
    assert isinstance(image, Figure)

    text = next(it)
    assert isinstance(text, str)
    assert text == "\n\na"


def test_convert_source_only(store: Store):
    markdown = "![a](matplotlib.ipynb){#matplotlib source=only}"
    x = list(convert(markdown, store))
    assert len(x) == 1


def test_convert_image_stdout(store: Store):
    markdown = "![a](matplotlib.ipynb){#stdout}"
    it = convert(markdown, store)
    text = next(it)
    assert isinstance(text, str)
    assert text == "1"


def test_convert_execute(store: Store):
    nb = store.get_notebook("matplotlib.ipynb")
    nb.is_executed = False
    markdown = "![a](matplotlib.ipynb){#matplotlib exec=1}"
    list(convert(markdown, store))
    assert nb.is_executed


def test_convert_active_notebook(store: Store):
    markdown = "![](a.ipynb){#_}"
    assert list(convert(markdown, store)) == []
    markdown = "![](){#a}"
    assert list(convert(markdown, store)) == ["1"]
    markdown = "![](b.ipynb){#_}"
    assert list(convert(markdown, store)) == []
    markdown = "![](){#b}"
    assert list(convert(markdown, store)) == ["2"]


def test_convert_other_format(store: Store):
    markdown = "![a](a.png){#fig}"
    it = convert(markdown, store)

    x = list(it)
    assert len(x) == 1
    assert isinstance(x[0], str)
    assert x[0] == "![a](a.png){#fig}"
