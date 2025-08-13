from __future__ import annotations

import html
import textwrap
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from nbsync import logger
from nbsync.markdown import is_truelike

if TYPE_CHECKING:
    from nbstore.markdown import Image


@dataclass
class Attributes:
    source: str
    tabs: str
    identifier: str
    result: str

    @classmethod
    def pop(cls, attrs: dict[str, str]) -> Attributes:
        return cls(
            source=attrs.pop("source", ""),
            tabs=attrs.pop("tabs", ""),
            identifier=attrs.pop("identifier", ""),
            result=attrs.pop("result", ""),
        )


@dataclass
class Cell:
    image: Image
    """The image instance from the Markdown file."""

    language: str
    """The language of the source to be used to generate the image."""

    mime: str
    """The MIME type of the image."""

    content: bytes | str
    """The content of the image."""

    def convert(self, *, escape: bool = False) -> str:
        attrs = Attributes.pop(self.image.attributes)

        if include_attrs := self._include_attributes():
            self.image.url = ""

        source = get_source(
            self,
            console=attrs.source == "console",
            include_attrs=include_attrs,
            include_identifier=bool(attrs.identifier),
        )

        if not self.content or attrs.source in ["console", "only"]:
            attrs.source = "only" if self.image.source else ""
            result = ""

        elif self.mime.startswith("text/") and isinstance(self.content, str):
            result = get_text_markdown(self, attrs.result, escape=escape)

        else:
            result = get_image_markdown(self)

        if markdown := get_markdown(attrs.source, source, result, attrs.tabs):
            return textwrap.indent(markdown, self.image.indent)

        return ""  # no cov

    def _include_attributes(self) -> bool:
        if "/" not in self.mime or not self.content:
            return True

        return self.mime.startswith("text/") and isinstance(self.content, str)


def get_source(
    cell: Cell,
    *,
    console: bool = False,
    include_attrs: bool = False,
    include_identifier: bool = False,
) -> str:
    if not (source := cell.image.source):
        return ""

    if console:
        output = str(cell.content.rstrip())
        source = f"{_add_prompt(source)}\n{output}"

    attrs = [cell.language]
    if include_attrs:
        attrs.extend(cell.image.iter_parts())
    attr = " ".join(attrs)

    if include_identifier:
        source = f"# #{cell.image.identifier}\n{source}"

    return f"```{attr}\n{source}\n```"


def _add_prompt(source: str) -> str:
    lines = []
    for line in source.splitlines():
        if not line:
            lines.append("")
        elif line.startswith(" "):
            lines.append(f"... {line}")
        else:
            lines.append(f">>> {line}")
    return "\n".join(lines)


def get_text_markdown(cell: Cell, result: str, *, escape: bool = False) -> str:
    text = str(cell.content.rstrip())

    if result:
        result = "text" if is_truelike(result) else result
        return f"```{result}\n{text}\n```"

    if escape and cell.mime == "text/plain":
        return html.escape(text)

    return text


def get_image_markdown(cell: Cell) -> str:
    msg = f"{cell.image.url}#{cell.image.identifier} [{cell.mime}]"
    logger.debug(f"Converting image: {msg}")

    if "/" not in cell.mime:
        cell.image.url = ""
        return ""

    ext = cell.mime.split("/")[1].split("+")[0]
    cell.image.url = f"{uuid.uuid4()}.{ext}"

    attr = " ".join(cell.image.iter_parts(include_identifier=True))
    return f"![{cell.image.alt}]({cell.image.url}){{{attr}}}"


def get_markdown(kind: str, source: str, result: str, tabs: str) -> str:
    if all(not x for x in (kind, source, result)):
        return ""

    if not kind or not source:
        return result

    if kind == "only":
        return source

    if is_truelike(kind) or kind == "above":
        return f"{source}\n\n{result}"

    if kind == "below":
        return f"{result}\n\n{source}"

    if kind == "material-block":
        result = f'<div class="result" markdown="1">\n{result}\n</div>'
        return f"{source}\n\n{result}"

    if kind == "tabbed-left":
        tabs = tabs if "|" in tabs else "Source|Result"
        return get_tabbed(source, result, tabs)

    if kind == "tabbed-right":
        tabs = tabs if "|" in tabs else "Result|Source"
        return get_tabbed(result, source, tabs)

    return result


def get_tabbed(left: str, right: str, tabs: str) -> str:
    left_title, right_title = tabs.split("|", 1)
    left = textwrap.indent(left, "    ")
    left = f'===! "{left_title}"\n\n{left}'
    right = textwrap.indent(right, "    ")
    right = f'=== "{right_title}"\n\n{right}'
    return f"{left}\n\n{right}\n"
