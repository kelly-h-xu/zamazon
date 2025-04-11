# IMPORTS
from flask import request,jsonify, abort, Blueprint
from flask_login import login_user, logout_user, current_user
from app import csrf
from .models.user import User
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
# from werkzeug.urls import url_parse

import pdb

# Create the blueprint
bp = Blueprint('users', __name__)

# Flask Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

# ____________
# METHOD
# LOGIN: Handles user login through GET and POST requests
@bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    # Check for users already logged in (should not happen)
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'}), 200  

    # Flask form
    form = LoginForm()

    if request.method == 'POST':
        # Validate the form
        if form.validate_on_submit():
            # Authenticate the user using provided credentials
            user = User.get_by_auth(form.email.data, form.password.data)
            
            # Authentication fails
            if user is None:
                return jsonify({'message': 'Invalid email or password'}), 401

            # Authentication succeeds, log in the user
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200

        # Form validation fails
        return jsonify({'message': 'Invalid form submission', 'errors': form.errors}), 400

    # Login required for GET request
    return jsonify({'message': 'Login required'}), 401

# ____________
# METHOD
# REGISTER: Handles user registration by accepting user details via POST request
@bp.route('/register', methods=['POST'])
def register():
    # Check for users already logged in (should not happen)
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'}), 400

    data = request.get_json()
    # Extract the data from the JSON request
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    address = data.get('address')
    password = data.get('password')

    # Validate form data
    if not firstname or not lastname or not email or not address or not password:
        return jsonify({'message': 'Missing fields in request data'}), 400
    

    if User.email_exists(email):  
        return jsonify({'message': 'An account with this email already exists.'}), 400
    
    # Register user using .register method of User object
    user = User.register(
        email=email,
        password=password,
        address=address,
        balance=0,  
        firstname=firstname,
        lastname=lastname
    )
    # On successful registration, route to /login, else fail
    if user:
        return jsonify({'message': 'Registration successful', 'user_id': user.uid}), 201
    else:
        return jsonify({'message': 'Registration failed. Please try again.'}), 500
# ____________
# METHOD
# SEARCH USERS
@bp.route('/user_search/<int:user_id>', methods=['GET'])
def search_users(user_id):
    # Fetch user information using the get function
    user = User.get(user_id)
    
    # User is not found
    if not user:
        abort(404, description="User not found")
    
    # Return user information as JSON
    return jsonify({
        'user_id': user.uid,
        'name': f"{user.firstname} {user.lastname}"
    })

# ____________
# METHOD
# LOGOUT: Handle user logout using POST request
@bp.route('/logout', methods=['POST'])
@csrf.exempt
def logout():
    # 
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# ____________
# METHOD
# AUTH CHECK: Check user authentication using GET request
@bp.route('/auth-check', methods=['GET'])
def auth_check():
    # Successful authentication
    if current_user.is_authenticated:
        return jsonify({'message': 'User is authenticated'}), 200
    
    # User authentication fails
    return jsonify({'message': 'User not authenticated'}), 401

# ____________
# METHOD
# USER DETAILS: Get public user details using GET request
@bp.route('/user/<int:user_id>', methods=['GET'])
def user_details(user_id):
    # Load in the user details
    user = User.get(user_id)

    # User does not exist
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Create the return object
    user_data = {
        'user_id': user.uid,
        'firstname': user.firstname,
        'lastname': user.lastname,
    }

    # Return the data as a JSON
    return jsonify(user_data), 200

# ____________
# BACKEND Registration Form
# class RegistrationForm(FlaskForm):
#     firstname = StringField('First Name', validators=[DataRequired()])
#     lastname = StringField('Last Name', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     address = StringField('Address', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField(
#         'Repeat Password', validators=[DataRequired(),
#                                        EqualTo('password')])
#     submit = SubmitField('Register')

#     def validate_email(self, email):
#         if User.email_exists(email.data):
#             raise ValidationError('Already a user with this email.')