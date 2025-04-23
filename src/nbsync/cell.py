from __future__ import annotations

import textwrap
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

from nbsync import logger
from nbsync.markdown import is_truelike

if TYPE_CHECKING:
    from nbstore.markdown import Image


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

    def convert(self) -> str:
        kind = self.image.attributes.pop("source", "")
        tabs = self.image.attributes.pop("tabs", "")
        identifier = self.image.attributes.pop("identifier", "")

        if "/" not in self.mime or not self.content or kind == "source-only":
            if self.image.source:
                source = get_source(
                    self,
                    include_attrs=True,
                    include_identifier=bool(identifier),
                )
                kind = "only"
            else:
                source = ""
            result, self.image.url = "", ""

        elif self.mime.startswith("text/") and isinstance(self.content, str):
            source = get_source(
                self,
                include_attrs=True,
                include_identifier=bool(identifier),
            )
            result, self.image.url = self.content, ""
            result = result.rstrip()

        else:
            source = get_source(
                self,
                include_attrs=False,
                include_identifier=bool(identifier),
            )
            result = get_result(self)

        if markdown := get_markdown(kind, source, result, tabs):
            return textwrap.indent(markdown, self.image.indent)

        return ""  # no cov


def get_source(
    cell: Cell,
    *,
    include_attrs: bool = False,
    include_identifier: bool = False,
) -> str:
    attrs = [cell.language]
    if include_attrs:
        attrs.extend(cell.image.iter_parts())
    attr = " ".join(attrs)

    source = cell.image.source
    if include_identifier:
        source = f"# #{cell.image.identifier}\n{source}"

    return f"```{attr}\n{source}\n```"


def get_result(cell: Cell) -> str:
    msg = f"{cell.image.url}#{cell.image.identifier} [{cell.mime}]"
    logger.debug(f"Converting image: {msg}")

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
        result = f'<div class="result" markdown="1">{result}</div>'
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
