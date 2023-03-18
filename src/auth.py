from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from src.constants.http_status_codes import *
from src.database import User, db
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    if len(password) < 6:
        return jsonify({'error': 'Short password'}), HTTP_400_BAD_REQUEST

    if len(username) < 4:
        return jsonify({'error': 'Short username'}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': 'Username should contain alfa and numeric'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Username must contain only alfa and numeric'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email is already taken'}), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username is already taken'}), HTTP_409_CONFLICT

    password_hash = generate_password_hash(password)

    user = User(username=username, password=password_hash, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': "User created",
                    'user': {
                        'username': username, 'email': email
                    }
                    }), HTTP_201_CREATED

    return ('User created successfully')


@auth.get('/me')
def me():
    return {'user': 'me'}