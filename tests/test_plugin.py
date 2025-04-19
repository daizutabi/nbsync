import os
import shutil
import sys
from pathlib import Path

import pytest
from mkdocs.commands.build import build
from mkdocs.config import load_config
from mkdocs.config.defaults import MkDocsConfig

from nbsync.plugin import Config, Plugin


@pytest.fixture(scope="module")
def config_file():
    return Path(__file__).parent.parent / "mkdocs.yaml"


def test_config_file_exists(config_file: Path):
    assert config_file.exists()


@pytest.fixture(scope="module")
def mkdocs_config(config_file: Path):
    return load_config(str(config_file))


@pytest.fixture(scope="module")
def nbstore_plugin(mkdocs_config: MkDocsConfig):
    return mkdocs_config.plugins["nbsync"]


def test_nbstore_plugin(nbstore_plugin: Plugin):
    assert isinstance(nbstore_plugin, Plugin)
    assert isinstance(nbstore_plugin.config, Config)


@pytest.fixture(scope="module")
def nbstore_config(nbstore_plugin: Plugin):
    return nbstore_plugin.config


def test_nbstore_config(nbstore_config: Config):
    config = nbstore_config
    assert config.src_dir == ["../notebooks", "../scripts"]


@pytest.fixture
def config_plugin(tmp_path):
    dest = Path(tmp_path)
    root = Path(__file__).parent.parent
    config_file = root / "mkdocs.yaml"
    shutil.copy(config_file, dest)
    for src in ["docs", "notebooks", "scripts", "src", "tests"]:
        src_dir = root / src
        shutil.copytree(src_dir, dest / src)
    curdir = Path(os.curdir).absolute()
    os.chdir(dest)
    sys.path.insert(0, ".")
    config = load_config("mkdocs.yaml")
    plugin = config.plugins["nbsync"]
    assert isinstance(plugin, Plugin)
    plugin.__init__()

    yield config, plugin

    config.plugins.on_shutdown()
    sys.path.pop(0)
    os.chdir(curdir)


def test_on_config(config_plugin: tuple[MkDocsConfig, Plugin]):
    config, plugin = config_plugin
    plugin.on_config(config)
    assert plugin.store is not None


@pytest.fixture
def config(config_plugin):
    return config_plugin[0]


def test_build(config: MkDocsConfig):
    config.plugins.on_startup(command="build", dirty=False)
    plugin = config.plugins["nbsync"]
    assert isinstance(plugin, Plugin)

    build(config, dirty=False)


def test_on_page_markdown_fallback():
    class FakePlugin(Plugin):
        pass

    plugin = FakePlugin()
    plugin.__class__.store = None
    assert plugin.on_page_markdown("abc", None, None) == "abc"  # type: ignore


def test_src_dir_list(config_plugin: tuple[MkDocsConfig, Plugin]):
    config, plugin = config_plugin
    src_dir = plugin.config.src_dir
    plugin.config.src_dir = ["a", "b"]
    plugin.on_config(config)
    assert plugin.store
    assert plugin.store.src_dirs[0].name == "a"
    assert plugin.store.src_dirs[1].name == "b"
    plugin.config.src_dir = src_dir
