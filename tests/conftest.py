import pytest
from nbstore.store import Store


@pytest.fixture(scope="session")
def store():
    return Store("tests/notebooks")
