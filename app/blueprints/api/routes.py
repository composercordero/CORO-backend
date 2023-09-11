from . import api
from app import db
from app.models import Conductor
from flask import request
from .auth import basic_auth, token_auth

# GET TOKEN --------------------------------

@api.route('/token')
@basic_auth.login_required
def get_token():
    auth_user = basic_auth.current_user()
    token = auth_user.get_token()
    return {'token': token,
            'token_exp': auth_user.token_expiration}

# GET ME --------------------------------

@api.route('/user/me')
@token_auth.login_required
def get_me():
    me = token_auth.current_user()
    return me.to_dict()

# CREATE USER --------------------------------

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

# LOGIN USER --------------------------------

@api.route('/login', methods=["GET"])
@basic_auth.login_required
def login_user():
    logged_in_user = basic_auth.current_user()
    return logged_in_user.to_dict(),201

# EDIT USER --------------------------------

@api.route('/users', methods=["PUT"])
@token_auth.login_required
def edit_user():
# def edit_user(user_data, token):
    auth_user = token_auth.current_user()
    data = request.json
    for field in data:
        if field in {'first_name', 'last_name', 'username', 'email', 'password'}:
            setattr(auth_user, field, data[field])
    db.session.commit()
    return auth_user.to_dict(),201

# DELETE USER --------------------------------

@api.route('/users', methods=["DELETE"])
@token_auth.login_required
def delete_user():
# def edit_user(user_data, token):
    auth_user = token_auth.current_user()
    db.session.delete(auth_user)
    db.session.commit()
    return {'success': f"{auth_user.first_name} has been deleted"}, 201