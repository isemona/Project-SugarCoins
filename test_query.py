from query import get_user_list_of_food
from flask_sqlalchemy import SQLAlchemy

def test_get_user_list_of_food():
    assert(type(get_user_list_of_food) == dict)

