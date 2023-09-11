from . import api
from app import db
from app.models import Conductor
from flask import request
from .auth import basic_auth, token_auth

@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token,
            'token_exp': auth_user.token_expiration}

@api.route('/user/me')
@token_auth.login_required
def get_me():
    me = token_auth.current_user()
    return me.to_dict()

@api.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return{'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['firstName', 'lastName', 'username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        if missing_fields:
            return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
        
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    check_user = db.session.execute(db.select(Conductor).where((Conductor.username == username) | (Conductor.email == email))).scalar()

    if check_user:
        {'error': f'A user with that username and/or email already exists'}, 400

    new_user = Conductor(first_name = first_name, last_name = last_name, username = username, email = email, password = password)

    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict(),201