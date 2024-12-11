# IMPORTS
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from .models.user import User

# Create the blueprint
bp = Blueprint('account', __name__)

# ____________
# METHOD
# ACCOUNT: Gets all the data for a user's account page
@bp.route('/account', methods=['GET'])
@login_required
def account():
    # Grab the current user
    user = current_user

    # Return their data as a JSON
    return jsonify({
        "user_id": user.uid,
        "email": user.email,
        "address": user.address,
        "balance": user.balance,
        "firstname": user.firstname,
        "lastname": user.lastname
    }), 200

# ____________
# METHOD
# UPDATE ACCOUNT: Updates a singular field in a user database entry 
@bp.route('/account/update/<field>', methods=['PATCH'])
@login_required
def update_account(field):
    # Ensure user is authenticated
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401

    # Get the new value from the request
    data = request.get_json()

    if not data or 'value' not in data:
        return jsonify({'message': 'Missing value to update'}), 400

    # Check updated email doesn't already exist
    if field == 'email':
        if User.email_exists(data['value']):
            return jsonify({'message': 'An account with this email already exists.'}), 400

    new_value = data['value']

    # Update the user's field using the model method
    updated_user = User.update_user(current_user.uid, field, new_value)
    
    # User update successful
    if updated_user:
        return jsonify({
            'message': f"{field} updated successfully",
            'updated_field': field,
            'new_value': getattr(updated_user, field)
        }), 200
    
    # Handle errors
    else:
        return jsonify({'message': 'Failed to update user details'}), 500
