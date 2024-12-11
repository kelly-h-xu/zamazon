from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
# from .models.purchase import Purchase
from .models.buys import Buys
from .models.seller_review import SellerReview
from .models.product_review import ProductReview

import pdb

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(0)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Buys.get_buys_by_buyer(current_user.id)
        # purchases = Buys.get_buys_by_buyer(1)
        # print(f"Purchases for user 1: {[purchase for purchase in purchases]}")
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)