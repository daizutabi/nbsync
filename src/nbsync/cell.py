from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

    from nbstore.markdown import Image


@dataclass
class Cell:
    image: Image
    """The image instance from the Markdown file."""

    source: str
    """The source used to generate the image."""

    kind: str
    """The kind of cell. Set from the source attribute of the image."""

    mime: str
    """The MIME type of the image."""

    content: bytes | str
    """The content of the image."""

    uri: str = field(default="", init=False)
    """The source URI of the image in MkDocs."""

    def convert(self) -> Self | str:
        if self.mime.startswith("text/") and isinstance(self.content, str):
            return self.content

        ext = self.mime.split("/")[1].split("+")[0]
        self.uri = f"{uuid.uuid4()}.{ext}"
        return self

    @property
    def markdown(self) -> str:
        src = self.uri or self.image.url
        attr = " ".join(self.image.iter_parts(include_identifier=True))
        return f"![{self.image.alt}]({src}){{{attr}}}"
