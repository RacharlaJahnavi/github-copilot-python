import pytest

import app as app_module


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    app_module.current_puzzle = None
    app_module.current_solution = None

    with app_module.app.test_client() as test_client:
        yield test_client

    app_module.current_puzzle = None
    app_module.current_solution = None
