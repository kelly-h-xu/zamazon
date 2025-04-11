from flask import render_template
from flask import jsonify, request
from flask_login import current_user, login_required

from .models.product import Product
from .models.user import User
from .models.seller import Seller
from .models.category import Category

import pdb

from flask import Blueprint
bp = Blueprint('inventory', __name__)

# get static list of categories
@bp.route('/categories', methods=['GET'])
def get_categories():
    ret = Category.get_categories()
    print(ret)
    return {'categories':[c.category_name for c in ret]}

# change quantity of an item in stock
@bp.route('/increase_stock', methods=['POST'])
def increase_stock():
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')
    return jsonify(Seller.change_product_quantity(product_id, quantity))

# change price of an item in stock
@bp.route('/change_price', methods=['POST'])
def change_price():
    product_id = request.json.get('product_id')
    price = request.json.get('price')
    return jsonify(Seller.change_product_price(product_id, price))

# Check if the current user is a seller
@bp.route('/is_seller', methods=['GET'])
def is_seller():
    seller_id = current_user.uid
    result = Seller.is_seller(seller_id)
    if result == 0:
        status = False
    else:
        status = True
    
    return {'seller_status': status}

# check if a given user is a seller
@bp.route('/is_seller/<seller_id>', methods=['GET'])
def is_seller_id(seller_id):
    seller_id = seller_id
    result = Seller.is_seller(seller_id)
    if result == 0:
        status = False
    else:
        status = True
    
    return {'seller_status': status}

# update product catalog table with new info
@bp.route('/update_catalog', methods=['POST'])
def update_product():
    name = request.json.get('product_name')
    category = request.json.get('category')
    description = request.json.get('description')
    image_url = request.json.get('image_url')
    return {'success':Seller.update_product_catlog(name,category,image_url,description)}

# fulfill an order item
@bp.route('/fulfill_item', methods=['POST'])
def fulfill_item():
    purchase_id = request.json.get('purchase_id')
    product_id = request.json.get('product_id')
    return {'fulfilled':Seller.fulfill_order_item(purchase_id, product_id)}

# add a new product to the catalog
@bp.route('/add_to_catalog', methods=['POST'])
def add_to_catalog():
    product_name = request.json.get('product_name')
    category = request.json.get('category')
    image_url = request.json.get('image_url')
    description = request.json.get('description')
    creator_id = current_user.uid
    return {'completed':Seller.add_product_to_catalog(product_name, category, description, image_url, creator_id)}

# set a listing as inactive so it doesn't appear in seller inventory
@bp.route('/remove_listing', methods=['POST'])
def remove_listing():
    product_id = request.json.get('product_id')
    x = Seller.remove_listing(product_id)
    print(x)
    return {'success': True}

# if name already in catalog, return its attributes, if not name is available
@bp.route('/check_availability', methods=['POST'])
def check_availability():
    product_name = request.json.get('product_name')
    result = Seller.verify_name_availability(product_name)
    ret = {'availability':True}
    if result != {}:
        ret['availability'] = False
        ret['description'] = result["description"]
        ret['image_url'] = result["image_url"]
        ret['category'] = result['category']
    return ret

# add a new product listing
@bp.route('/add_to_inventory', methods=['POST'])
def make_listing():
    if not Seller.is_seller(current_user.uid):
        Seller.add_seller(current_user.uid)
    product_name = request.json.get('product_name')
    seller_id = current_user.uid
    price = request.json.get('price')
    quantity = int(request.json.get('quantity'))
    
    return {'product': Seller.add_product_listing(product_name, seller_id, price, quantity)}

# get all fulfilled order items
@bp.route('/get_fulfilled_ordered_items', methods=['GET'])
def get_fulfilled_ordered_items():
    page = int(request.args.get('currentPage'))
    items_per_page = int(request.args.get('itemsPerPage'))
    items = []
    total = 0
    if current_user.is_authenticated:
        items, total = Seller.get_fulfilled_ordered_items_by_seller(current_user.uid, page, items_per_page)
    if not items:
        return jsonify({'fulfilled':[], 'total':0}), 200
    items_list = [
        {
            "product_id": p.product_id,
            'purchase_id': p.purchase_id,
            "order_quantity": p.order_quantity,
            "at_price": p.at_price,
            "fulfillment_time":p.fulfillment_time,
            "name" :p.name,
            "price" :p.price,
            "category":p.category,
            "description":p.description,
            "image_url":p.image_url,
            "product_quantity":p.product_quantity,
            "date_time":p.date_time,
            "fulfillment_status":str(p.fulfillment_status),
            'address' :p.address,
        } for p in items
    ]
    return jsonify({'fulfilled': items_list, 'total':total}), 200

# get all unfulfilled order items
@bp.route('/get_unfulfilled_ordered_items', methods=['GET'])
def get_unfulfilled_ordered_items():
    page = int(request.args.get('currentPage'))
    items_per_page = int(request.args.get('itemsPerPage'))
    items = []
    total = 0
    if current_user.is_authenticated:
        items, total = Seller.get_unfulfilled_ordered_items_by_seller(current_user.uid, page, items_per_page)
    if not items:
        return jsonify({'fulfilled':[], 'total':0}), 200
    items_list = [
        {
            "product_id": p.product_id,
            'purchase_id': p.purchase_id,
            "order_quantity": p.order_quantity,
            "at_price": p.at_price,
            "fulfillment_time":p.fulfillment_time,
            "name" :p.name,
            "price" :p.price,
            "category":p.category,
            "description":p.description,
            "image_url":p.image_url,
            "product_quantity":p.product_quantity,
            "date_time":p.date_time,
            "fulfillment_status":str(p.fulfillment_status),
            'address' :p.address,
            'fillable': p.product_quantity >= p.order_quantity
        } for p in items
    ]
    print(items_list)
    return jsonify({'unfulfilled': items_list, 'total':total}), 200

# get paginated inventory of active items
@bp.route('/my_inventory', methods=['GET'])
def get_inventory():
    page = int(request.args.get('currentPage'))
    items_per_page = int(request.args.get('itemsPerPage'))
    products = []
    total_items = 0
    if current_user.is_authenticated: 
        products, total_items = Seller.get_paginated_products_by_seller(current_user.uid, page, items_per_page)
        # empty case
    if not products:
        return jsonify({'products':[], 'total_items':0}), 200
    print(products)
    product_list = [
        {
            'id': product.product_id,
            'name': product.product_name,
            'price': product.price,
            'quantity': product.quantity,
            'category': product.category,
            'description': product.description,
            'image_url': product.image_url,
            'is_creator': True if product.creator_id == current_user.uid else False 
        } for product in products
    ]
    
    return {'products':product_list, 'total_items':total_items}, 200

# Get paginated products by seller for UserDetailPage
@bp.route('/get_paginated_products_by_seller/<int:seller_id>', methods=['GET'])
def get_paginated_products(seller_id):
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('page_size', 3)) # if no input stick to 3
    products, total_count = Seller.get_paginated_products_by_seller(seller_id, page, items_per_page)

    return jsonify({
        "products": [product.to_dict() for product in products],
        "total_count": total_count
    })

@bp.route('/fulfill-item/<purchase_id>/<product_id>', methods=['POST'])
# This is a trial route to check fulfillment stuff
def fulfill_an_item(purchase_id, product_id):
    # purchase_id = request.json.get('purchase_id')
    # product_id = request.json.get('product_id')
    return {'fulfilled':Seller.fulfill_order_item(purchase_id, product_id)}
