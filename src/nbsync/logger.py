from __future__ import annotations

import logging
from logging import Logger, LoggerAdapter
from typing import Any

_logger = logging.getLogger("nbsync")


def set_logger(logger: Logger | LoggerAdapter | None = None) -> Logger | LoggerAdapter:
    global _logger  # noqa: PLW0603

    if logger:
        _logger = logger

    return _logger


def debug(msg: str, *args: Any, **kwargs: Any) -> None:
    _logger.debug(msg, *args, **kwargs)


def info(msg: str, *args: Any, **kwargs: Any) -> None:
    _logger.info(msg, *args, **kwargs)


def warning(msg: str, *args: Any, **kwargs: Any) -> None:
    _logger.warning(msg, *args, **kwargs)


def error(msg: str, *args: Any, **kwargs: Any) -> None:
    _logger.error(msg, *args, **kwargs)
