# IMPORTS
from flask_login import current_user
from flask import jsonify, Blueprint, request
from .models.buys import Buys
from flask import request, jsonify

# Create the blueprint
bp = Blueprint('purchase_history', __name__)

# Get a list of purchase history objects
# TODO: If the order is fulfilled, we can write a review
# TODO: add seller name to display on this page (makes seller review easier to tell)

# ____________
# METHOD
# PURCHASE HISTORY: Get the purchase history for a user, paginated and ordered by the request
@bp.route('/purchase_history', methods=['GET'])
def get_purchase_history():
    # Check user is logged in
    if current_user.is_authenticated:
        # Get query parameters
        page = request.args.get('page', 1, type=int)  # Default to page 1
        items_per_page = request.args.get('items_per_page', 3, type=int)  # Default to 3 items per page
        sort_by = request.args.get('sort_by', 'date_time')  # Default sorting by date_time

        # Fetch paginated and sorted orders for the current user
        purchases = Buys.get_paginated_orders_by_buyer(current_user.id, page, items_per_page, sort_by)

        # Get total number of orders to calculate total pages
        total_orders = Buys.get_total_orders_by_buyer(current_user.id)  # Helper method to count total orders
        total_pages = (total_orders + items_per_page - 1) // items_per_page  # Ceiling division to calculate total pages

        # Return paginated purchases with total pages and total orders
        return jsonify({
            "purchases": purchases,
            "total_pages": total_pages,
            "total_orders": total_orders
        }), 200
    
    else:
        # User not logged in
        return jsonify({"message": "User not authenticated"}), 401
    
@bp.route('/get-all-buys', methods = ['GET'])
def all_buys_details ():
    # Load in the data using the model method
    details = Buys.get_all_buys()

    # Return the converted data as a JSON
    return jsonify([detail.__dict__ for detail in details]), 200

# ____________
# METHOD
# BUYS BY ORDER: Get all the products in a specific order
@bp.route('/buys-by-order/<int:order_id>', methods = ['GET'])
def order_details(order_id):
    # Load in the data using the model method
    details = Buys.get_buys_by_order(order_id)
    return jsonify({'items': details}), 200
