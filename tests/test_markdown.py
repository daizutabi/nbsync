import nbstore.markdown
import pytest
from nbstore.markdown import CodeBlock, Image, parse


def test_convert_image():
    from nbsync.markdown import convert_image

    text = "![a](b.ipynb){#c}"
    image = next(parse(text))
    assert isinstance(image, Image)
    image = next(convert_image(image))
    assert isinstance(image, Image)
    assert image.alt == "a"
    assert image.url == "b.ipynb"
    assert image.identifier == "c"


def test_convert_image_no_identifier():
    from nbsync.markdown import convert_image

    text = "![ a ]( b.ipynb ){  c ' b ' }"
    image = next(parse(text))
    assert isinstance(image, Image)
    text_ = next(convert_image(image))
    assert isinstance(text_, str)
    assert text_ == text


def test_convert_image_source_with_identifier():
    from nbsync.markdown import convert_image

    text = '![a](b.ipynb){#c `x=1` exec="1"}'
    image = next(parse(text))
    assert isinstance(image, Image)
    assert image.source
    it = convert_image(image)
    code_block = next(it)
    assert isinstance(code_block, CodeBlock)
    assert code_block.text == ""
    assert code_block.url == "b.ipynb"
    assert code_block.identifier == "c"
    assert code_block.classes == []
    assert code_block.attributes == {}

    image = next(it)
    assert isinstance(image, Image)
    assert image.text == text
    assert image.url == "b.ipynb"
    assert image.identifier == "c"
    assert image.classes == []
    assert image.attributes == {"exec": "1"}


def test_convert_image_source_without_identifier():
    from nbsync.markdown import convert_image

    text = '![a](b.ipynb){`x=1` exec="1"}'
    image = next(parse(text))
    assert isinstance(image, Image)
    it = convert_image(image)
    code_block = next(it)
    image = next(it)
    assert isinstance(code_block, CodeBlock)
    assert isinstance(image, Image)
    assert code_block.identifier == image.identifier


def test_convert_code_block():
    from nbsync.markdown import convert_code_block

    elems = nbstore.markdown.parse(SOURCE_TAB)
    code_block = list(elems)[0]
    assert isinstance(code_block, CodeBlock)
    elems = list(convert_code_block(code_block))
    assert isinstance(elems[0], str)
    assert elems[0].startswith("===")
    assert isinstance(elems[1], CodeBlock)
    assert elems[1].classes == ["python"]


def test_set_url():
    from nbsync.markdown import set_url

    image = Image("", "a", [], {}, "", "b.ipynb")
    image, url = set_url(image, "")
    assert isinstance(image, Image)
    assert url == "b.ipynb"


def test_set_url_not_supported_extension():
    from nbsync.markdown import set_url

    image = Image("abc", "a", [], {}, "", "b.txt")
    text, url = set_url(image, "a.ipynb")
    assert text == "abc"
    assert url == "a.ipynb"


@pytest.mark.parametrize("url", ["", "."])
def test_set_url_empty_url(url: str):
    from nbsync.markdown import set_url

    image = Image("abc", "a", [], {}, "", url)
    image, url = set_url(image, "a.ipynb")
    assert isinstance(image, Image)
    assert image.url == "a.ipynb"
    assert url == "a.ipynb"


def test_parse_url():
    from nbsync.markdown import parse_url

    images = [
        Image("abc", "a", [], {}, "", "a.py"),
        Image("abc", "a", [], {}, "", ""),
        Image("abc", "a", [], {}, "", "."),
    ]
    images = list(parse_url(images))
    for image in images:
        assert isinstance(image, Image)
        assert image.url == "a.py"


def test_parse_url_code_block():
    from nbsync.markdown import parse_url

    code_blocks = [CodeBlock("abc", "a", [], {}, "", "")]
    text = list(parse_url(code_blocks))[0]
    assert text == "abc"


def test_parse_url_str():
    from nbsync.markdown import parse_url

    text = list(parse_url(["abc"]))[0]
    assert text == "abc"


SOURCE = """\
![alt](a.py){#.}
![alt](){#id}
```python
a
```
```python {.#id2}
b
```
![alt](){`x=1`}
"""


@pytest.fixture(scope="module")
def elems():
    from nbsync.markdown import parse

    return list(parse(SOURCE))


def test_len(elems):
    assert len(elems) == 11


def test_elems_0(elems):
    image = elems[0]
    assert isinstance(image, Image)
    assert image.identifier == "."
    assert image.url == "a.py"


def test_elems_2(elems):
    image = elems[2]
    assert isinstance(image, Image)
    assert image.url == "a.py"
    assert image.identifier == "id"


def test_elems_4(elems):
    assert elems[4] == "```python\na\n```"


def test_elems_6(elems):
    code_block = elems[6]
    assert isinstance(code_block, CodeBlock)
    assert code_block.url == "a.py"
    assert code_block.identifier == "id2"
    assert code_block.source == "b"


def test_elems_8(elems):
    code_block = elems[8]
    assert isinstance(code_block, CodeBlock)
    assert code_block.url == "a.py"
    assert code_block.source == "x=1"


def test_elems_9(elems):
    image = elems[9]
    assert isinstance(image, Image)
    assert image.url == "a.py"
    assert image.identifier == elems[8].identifier


def test_elems_10(elems):
    assert elems[10] == "\n"


SOURCE_TAB = """\
````markdown source="tabbed-nbsync"
```python exec="on"
print("Hello Markdown from markdown-exec!")
```
````
"""
