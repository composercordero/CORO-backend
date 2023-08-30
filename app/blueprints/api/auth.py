from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app import db
from app.models import User
from datetime import datetime

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify(username, password):
    user = db.session.execute(db.select(User).where(User.username==username)).scalar()
    if user is not None and user.check_password(password):
        return user
    return None

@basic_auth.error_handler
def handle_error(status):
    return {'error': 'Incorrect username and/or password.'}, status

@token_auth.verify_token
def verify(token):
    user = db.session.execute(db.select(User).where(User.token == token)).scalar()
    if user is not None and user.token_expiration > datetime.utcnow():
        return user
    return None

@token_auth.error_handler
def handle_error(status):
    return {'error:' 'You do not have a valid token'}, status