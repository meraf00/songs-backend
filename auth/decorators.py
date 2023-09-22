from functools import wraps

from flask import jsonify, make_response, request

import auth.services as services

def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return make_response(jsonify({'message': 'Unauthorized'}), 401)
        
        try:
            user = services.verify_token(token)
        except:
            return make_response(jsonify({'message': 'Unauthorized'}), 401)
        
        return func(user, *args, **kwargs)

    return decorator