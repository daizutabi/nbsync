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
    it = convert_image(image, 0)
    code_block = next(it)
    image = next(it)
    assert isinstance(code_block, CodeBlock)
    assert isinstance(image, Image)
    assert code_block.identifier == image.identifier
    assert code_block.identifier == "image-nbsync-0"


def test_convert_image_source_without_identifier_error():
    from nbsync.markdown import convert_image

    text = '![a](b.ipynb){`x=1` exec="1"}'
    image = next(parse(text))
    assert isinstance(image, Image)
    with pytest.raises(ValueError, match="index is required"):
        list(convert_image(image))


SOURCE_TAB_CODE_BLOCK = """\
````markdown source="tabbed-nbsync"
```python exec="on"
print("Hello Markdown from markdown-exec!")
```
````
"""


def test_convert_tabbed_code_block_code_block():
    from nbsync.markdown import convert_code_block

    elems = nbstore.markdown.parse(SOURCE_TAB_CODE_BLOCK)
    code_block = list(elems)[0]
    assert isinstance(code_block, CodeBlock)
    elems = list(convert_code_block(code_block))
    assert isinstance(elems[0], str)
    assert elems[0].startswith("===")
    assert "tabbed-nbsync" not in elems[0]
    assert elems[1] == '=== "Rendered"\n\n'
    assert isinstance(elems[2], CodeBlock)
    assert elems[2].classes == ["python"]
    assert elems[2].source.startswith("print(")
    assert elems[2].text.startswith("    ```python")


SOURCE_TAB_IMAGE = """\
````markdown source="tabbed-nbsync"
![alt](a.py){#.}
````
"""


def test_convert_tabbed_code_block_image():
    from nbsync.markdown import convert_code_block

    elems = nbstore.markdown.parse(SOURCE_TAB_IMAGE)
    code_block = list(elems)[0]
    assert isinstance(code_block, CodeBlock)
    elems = list(convert_code_block(code_block))
    assert elems[1] == '=== "Rendered"\n\n'
    assert isinstance(elems[2], Image)
    assert elems[2].indent == "    "
    assert elems[2].text.startswith("    ![")


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


def test_resolve_urls():
    from nbsync.markdown import resolve_urls

    images = [
        Image("abc", "a", [], {}, "", "a.py"),
        Image("abc", "a", [], {}, "", ""),
        Image("abc", "a", [], {}, "", "."),
    ]
    images = list(resolve_urls(images))
    for image in images:
        assert isinstance(image, Image)
        assert image.url == "a.py"


def test_resolve_urls_code_block():
    from nbsync.markdown import resolve_urls

    code_blocks = [CodeBlock("abc", "a", [], {}, "", "")]
    text = list(resolve_urls(code_blocks))[0]
    assert text == "abc"


def test_resolve_urls_str():
    from nbsync.markdown import resolve_urls

    text = list(resolve_urls(["abc"]))[0]
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


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("1", True),
        ("0", False),
        ("yes", True),
        ("no", False),
        ("true", True),
        ("false", False),
        ("on", True),
        ("off", False),
    ],
)
def test_is_truelike(value, expected):
    from nbsync.markdown import is_truelike

    assert is_truelike(value) == expected
    assert is_truelike(value.upper()) == expected
