import pytest
from models import User


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password != 'FlaskIsAwesome' # hashed password != password
    assert new_user.phone == '1234567890'
    assert new_user.gender_code == 'M'
    
   
