import math
from flask import request
from flask import jsonify
from flask_login import current_user


from .models.product import Product
from .models.productCatalog import ProductCatalog
from .models.productListing import ProductListing


from flask import Blueprint
bp = Blueprint('products', __name__)


@bp.route('/products', methods=['GET'])
def get_products():
   category = request.args.get('category', "all", type=str)
   search_term = request.args.get('search', type=str)
   page = request.args.get('page', 1, type=int) #1 is the default
   filter = request.args.get('filter', "None", type=str) #None is the default
   limit = 16
   offset = (page - 1) * limit


   #default category is "all"
   if category == "flowers":
       category = "Flowers"
   elif category == "succulents":
       category = "Succulents"
   elif category == "herbs":
       category = "Herbs"
   elif category == "fruit-veg":
       category = "Fruits and Vegetables"


   #default filtering is None
   if filter == "None":
       column = None
       order_by = None
   elif filter == "price_low_high":
       column = 'price'
       order_by = 'ASC'
   elif filter == "price_high_low":
       column = 'price'
       order_by = 'DESC'
   elif filter== "avg_rating":
       column = 'avg_rating'
       order_by = 'DESC'
   elif filter == "total_purchases":
       column = 'total_purchases'
       order_by = 'DESC'


   products = ProductCatalog.get_products_by_category(category, search_term = search_term, column = column, order_by = order_by, limit = limit, offset = offset)
   total_products = ProductCatalog.get_total_products(category, search_term = search_term)
   total_pages = math.ceil(total_products/limit)


   return jsonify({
       'products': [product.__dict__ for product in products],
       'totalPages': total_pages
   })

@bp.route('/products_listings/<product_name>', methods=['GET'])
def get_listing_by_name(product_name):
    products = ProductListing.get_listing_by_name(product_name)
    return jsonify([product.__dict__ for product in products])

@bp.route('/products/<product_name>', methods=['GET'])
def get_product_by_name(product_name):
    products = ProductCatalog.get_product_by_name(product_name)
    return jsonify([product.__dict__ for product in products])

