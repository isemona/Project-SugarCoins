# This is default test configuration file used by pytest

import pytest
from server import app as app_object
from models import User

@pytest.fixture
def app():
    app = app_object
    app.debug = True
    return app

@pytest.fixture(scope='module')
def new_user():
    # Added other information to check e.g. name, gender_code, phone)
    new_user = User(name = "Pat Kennedy",
                    email='patkennedy79@gmail.com',
                    password='FlaskIsAwesome',
                    gender_code="M",
                    phone='1234567890')
    return new_user

