# This is default test configuration file used by pytest

import pytest
from server import app as app_object

@pytest.fixture
def app():
    app = app_object
    app.debug = True
    return app

