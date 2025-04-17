from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

    from .markdown import Element


@dataclass
class Figure:
    elem: Element
    """The element."""

    alt: str
    """The alternative text."""

    url: str
    """The Notebook URL."""

    mime: str = ""
    """The MIME type of the image."""

    content: bytes | str = ""
    """The content of the image."""

    src: str = ""
    """The source URI of the image in MkDocs."""

    @classmethod
    def from_element(cls, elem: Element) -> Self:
        alt = getattr(elem, "alt", "")
        url = getattr(elem, "url", "")
        return cls(elem, alt, url)

    def convert(self, mime: str, content: bytes | str) -> Self | str:
        if mime.startswith("text/") and isinstance(content, str):
            return content

        self.mime = mime
        self.content = content
        self.src = f"{uuid.uuid4()}.{get_suffix(mime)}"
        return self

    @property
    def markdown(self) -> str:
        src = self.src or self.url
        attr = " ".join(self.elem.iter_parts(include_identifier=True))
        return f"![{self.alt}]({src}){{{attr}}}"


def get_suffix(mime: str) -> str:
    return mime.split("/")[1].split("+")[0]
