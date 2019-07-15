# test_app.py
import pytest
from flask import url_for



def test_index(client):
    res = client.get(url_for('index'))
    assert res.status_code == 200
    assert b'Track your sugar coin spending today', res.data

def test_register_form(client):
    res = client.get(url_for('register_form'))
    assert res.status_code == 200
    assert b'Register', res.data
#
# def test_login_form(client):
#     res = client.get(url_for('login_form'))
#     assert res.status_code == 200
#
#
# def test_logout_form(client):
#     res = client.get(url_for('logout'))
#     assert res.status_code == 200

# def test_intake_form(client):
#     res = client.get(url_for('intake_form'))
#     assert res.status_code == 200

# def test_user_dashboard_main(client):
#     res = client.get(url_for('user_dashboard_main'))
#     assert res.status_code == 200

# def user_profile(client):
#     res = client.get(url_for('user_profile'))
#     assert res.status_code == 200

# def test_user_weight_trends(client):
#     res = client.get(url_for('user_weight_trends'))
#     assert res.status_code == 200

# def test_user_glucose_trends(client):
#     res = client.get(url_for('user_glucose_trends'))
#     assert res.status_code == 200

# def test_user_trends(client):
#     res = client.get(url_for('user_trends'))
#     assert res.status_code == 200
#
# def test_user_mood_trends(client):
#     res = client.get(url_for('user_mood_trends'))
#     assert res.status_code == 200
#
# def test_user_percent_intake(client):
#     res = client.get(url_for('user_percent_intake'))
#     assert res.status_code == 200
#
# def test_user_monthly_intake(client):
#     res = client.get(url_for('user_monthly_intake'))
#     assert res.status_code == 200

# def test_sms_ahoy_reply(client):
#     res = client.get(url_for('sms_ahoy_reply'))
#     assert res.status_code == 200




