from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from mkdocs.config import Config as BaseConfig
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from nbstore.store import Store

from .logger import logger
from .sync import Synchronizer

if TYPE_CHECKING:
    from typing import Any

    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.files import Files
    from mkdocs.structure.pages import Page

    from .cell import Cell


class Config(BaseConfig):
    """Configuration for Nbstore plugin."""

    src_dir = config_options.Type((str, list), default=".")


class Plugin(BasePlugin[Config]):
    store: ClassVar[Store | None] = None
    syncs: ClassVar[dict[str, Synchronizer]] = {}
    files: Files

    def on_config(self, config: MkDocsConfig, **kwargs: Any) -> MkDocsConfig:
        if isinstance(self.config.src_dir, str):
            src_dirs = [self.config.src_dir]
        else:
            src_dirs = self.config.src_dir

        src_dirs = [(Path(config.docs_dir) / s).resolve() for s in src_dirs]

        store = self.__class__.store

        if store is None or store.src_dirs != src_dirs:
            self.__class__.store = Store(src_dirs)
            config.watch.extend(x.as_posix() for x in src_dirs)

        for name in ["attr_list", "md_in_html"]:
            if name not in config.markdown_extensions:
                config.markdown_extensions.append(name)

        return config

    def on_files(self, files: Files, config: MkDocsConfig, **kwargs: Any) -> Files:
        self.files = files
        return files

    def on_page_markdown(
        self,
        markdown: str,
        page: Page,
        config: MkDocsConfig,
        **kwargs: Any,
    ) -> str:
        if self.__class__.store is None:
            msg = "Store must be initialized before processing markdown"
            logger.error(msg)
            return markdown

        src_uri = page.file.src_uri
        syncs = self.__class__.syncs

        if src_uri not in syncs:
            syncs[src_uri] = Synchronizer(self.__class__.store)

        markdowns = []

        for elem in syncs[src_uri].convert(markdown):
            if isinstance(elem, str):
                markdowns.append(elem)

            elif markdown := elem.convert():
                markdowns.append(markdown)

                if elem.image.url and elem.content:
                    file = generate_file(elem, src_uri, config)
                    self.files.append(file)

        return "".join(markdowns)


def generate_file(cell: Cell, page_uri: str, config: MkDocsConfig) -> File:
    src_uri = (Path(page_uri).parent / cell.image.url).as_posix()
    return File.generated(config, src_uri, content=cell.content)
