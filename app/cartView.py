from flask import Blueprint, request, jsonify
from flask import render_template
from flask_login import current_user, login_required
from app.controllers.cartManager import CartManager
from app.models.cartDAL import CartDAL


# CartView
bp = Blueprint('carts', __name__)

@bp.route('/carts', methods=['GET'])
@login_required
def get_cart_items():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401
    items, total_price = CartManager.get_cart_for_user(current_user.uid)
    
# we have empty cart
    if not items:
        return jsonify({'message': 'Your cart is empty', 'items': [], 'total_price': 0}), 200
    # instead of rendering an HTML page previously, make sure it returns a JSON for the React to recieve the data. 
    return jsonify({'items': items, 'total_price': total_price}), 200

@bp.route('/get-paginated-carts', methods=['GET'])
@login_required
def get_paginated_cart_items():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401

    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('itemsPerPage', 5))

    items, total_price, total_pages = CartManager.get_paginated_carts_by_user(current_user.uid, page, items_per_page)

    if not items:
        return jsonify({'message': 'Your cart is empty', 'items': [], 'total_price': 0, 'total_pages': 0}), 200

    return jsonify({
        'items': items,
        'total_price': total_price,
        'total_pages': total_pages
    }), 200


@bp.route('/add-to-cart/<product_id>', methods = ['POST'])
def add_item_to_cart(product_id):
    success = CartManager.add_item_to_cart(current_user.uid, product_id)
    if success:
        return jsonify({"status": "Item added successfully"}), 200
    else:
        return jsonify({"status": "Failed to add"}), 500

@bp.route('/delete-item/<int:product_id>', methods = ['DELETE'])
def remove_item_from_cart(product_id):
    success = CartManager.delete_item_from_cart(current_user.uid,product_id)
    if success:
        return jsonify({"status": "Item removed successfully"}), 200
    else:
        return jsonify({"status": "Failed to remove"}), 500

@bp.route('/decrease-quantity/<int:product_id>', methods = ['PATCH'])
def decrease_quantity(product_id):
    new_quantity = CartManager.decrease_quantity(current_user.uid, product_id)
    return jsonify(new_quantity), 200

@bp.route('/clear-cart', methods = ['DELETE'])
def clear_cart():
    success = CartManager.clear_cart(current_user.uid)
    if success:
        return jsonify({"status": "Cart is cleared"}), 200
    else:
        return jsonify({"status": "Failed :("}), 500

@bp.route('/check-stock/<int:product_id>', methods = ['GET'])
def check_stock(product_id):
    quantity = CartManager.check_product_stock(product_id)
    return jsonify(quantity), 200

@bp.route('/check-balance/<int:user_id>', methods = ['GET'])
def check_balance(user_id):
    quantity = CartManager.check_user_balance(user_id)
    return jsonify(quantity), 200


# @bp.route('/place-order', methods = ['POST'])
# def submit_order():
#     if not current_user.is_authenticated:
#         return jsonify({'message': 'Unauthorized'}), 401
#     success = CartManager.place_order(current_user.uid)
#     if success:
#         return jsonify({"status": "Order added successfully"}), 200
#     else:
#         return jsonify({"status": "Failed to place order"}), 500

@bp.route('/place-order', methods=['POST'])
def submit_order():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401

    response = CartManager.place_order(current_user.uid)
    
    if response.get("success"):
        return jsonify({
            "status": "Order added successfully",
            "purchase_id": response["purchase_id"],
            "date_time": response["date_time"]
        }), 200
    else:
        return jsonify({
            "status": "Failed to place order",
            "error": response["error"]
        }), 400  

@bp.route('/update-balance', methods = ['PATCH'])
def update():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized'}), 401
    success = CartDAL.update_balance(current_user.uid)
    if success:
        return jsonify ({"status": "yay"}), 200


