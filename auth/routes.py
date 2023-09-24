from flask import Blueprint, make_response, jsonify, request
from auth.decorators import login_required
import auth.services as services
from auth.serilizers import UserSerializer

auth_bp = Blueprint('user', __name__)

@auth_bp.route('/')
@login_required
def get_user(user):
    response = UserSerializer.serialize(user)

    return make_response(jsonify(response), 200)
    

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if services.verify_credentials(email, password):
        user = services.get_user_by_email(email)
        token = services.generate_auth_token(user)

        return make_response(jsonify({'token': token}), 200)
    
    return make_response(jsonify({'message': 'Invalid credentials'}), 401)
    

@auth_bp.route('/signup', methods=['POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return make_response(jsonify({'message': 'Email and password are required'}), 400)

    try:
        user = services.create_user(email, password)
        token = services.generate_auth_token(user)

        return make_response(jsonify({'token': token}), 200)
    except:
        return make_response(jsonify({'message': 'User already exists.'}), 409)

