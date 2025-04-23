import logging
from logging import Logger

import pytest

from nbsync import logger


@pytest.fixture
def reset_logger():
    original_logger = logger._logger

    yield

    logger._logger = original_logger


def test_default_logger():
    assert isinstance(logger._logger, Logger)
    assert logger._logger.name == "nbsync"


def test_configure(reset_logger):
    custom_logger = logging.getLogger("custom_logger")

    result = logger.configure(custom_logger)

    assert result is custom_logger
    assert logger._logger is custom_logger
    assert logger._logger.name == "custom_logger"


def test_configure_no_args(reset_logger):
    custom_logger = logging.getLogger("custom_logger")
    logger._logger = custom_logger

    result = logger.configure()

    assert result is custom_logger
    assert logger._logger is custom_logger


def test_logging_methods(reset_logger, caplog):
    caplog.set_level(logging.DEBUG, logger="nbsync")

    debug_msg = "Debug message"
    info_msg = "Info message"
    warning_msg = "Warning message"
    error_msg = "Error message"

    logger.debug(debug_msg)
    logger.info(info_msg)
    logger.warning(warning_msg)
    logger.error(error_msg)

    assert debug_msg in caplog.text
    assert info_msg in caplog.text
    assert warning_msg in caplog.text
    assert error_msg in caplog.text

    assert (logger._logger.name, logging.DEBUG, debug_msg) in caplog.record_tuples
    assert (logger._logger.name, logging.INFO, info_msg) in caplog.record_tuples
    assert (logger._logger.name, logging.WARNING, warning_msg) in caplog.record_tuples
    assert (logger._logger.name, logging.ERROR, error_msg) in caplog.record_tuples
