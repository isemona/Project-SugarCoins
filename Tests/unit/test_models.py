from models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """

    # Added other information to check e.g. name, gender_code, phone)
    new_user = User(name = "Pat Kennedy",
                    email='patkennedy79@gmail.com',
                    password='FlaskIsAwesome',
                    gender_code="M",
                    phone='1234567890')
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password == 'FlaskIsAwesome'
    assert new_user.phone == '1234567890'
    assert new_user.gender_code == 'M'
    # assert not new_user.authenticated
