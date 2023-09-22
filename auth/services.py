from auth.models import User
from db import db
import jwt
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from typing import Optional

def get_user_by_id(id: int) -> User:
    user = User.query.filter_by(id=id).first()

    return user

def get_user_by_email(email: str) -> User:
    user = User.query.filter_by(email=email).first()

    return user


def create_user(email: str, password: str) -> User:
    user = User(
        email=email,
        password=generate_password_hash(password)
    )

    db.session.add(user)
    db.session.commit()

    return user


def generate_auth_token(user: User) -> Optional[str]:
    jwt_exp = timedelta(days=1)

    claim = {
        'email': user.email,
        'exp': datetime.now() + jwt_exp
    }

    token  = jwt.encode(claim, os.getenv('FLASK_SECRET_KEY'), algorithm='HS256')
    
    return token


def verify_token(token: str) -> Optional[User]:
    try:
        claim = jwt.decode(token, os.getenv('FLASK_SECRET_KEY'), algorithms=['HS256'])
        user = User.query.filter_by(email=claim['email']).first()

        return user
    except Exception as e:        
        return None
    

def verify_credentials(email: str, password: str) -> bool:
    user = User.query.filter_by(email=email).first()

    if not user:
        return False

    return check_password_hash(user.password, password)        
    