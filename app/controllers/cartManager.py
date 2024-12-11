from flask import current_app as app
from flask import render_template
from app.models.cartDAL import CartDAL
from app.models.order import OrderDAL

# use the cart manager as the responsible entity for the orders as well. 
# This is where you specify the edge cases or check everything before passing it into the DAL.
# So essentially the DAL is assuming a perfect world bc if not the manager should reject it before the dal gets
# the request. 
# Handle the orderDAL and CartDAL

class CartManager:
    # manage the entire cart 
    # think of cart as a manager that calls the dal which is cart contains
    # To do : check sttaus of like product id blah blah that it exists. 
    def __init__(self, uid, total_price):
        self.uid = uid
        self.total_price = total_price

    @staticmethod
    def check_user_balance(uid):
        rows = CartDAL.get_user_balance(uid)
        if not rows:
            raise Exception("User not found")
        user_balance = rows [0][0]
        return user_balance

    @staticmethod
    def check_product_stock(product_id):
        rows = CartDAL.get_product_stock(product_id)
        if not rows:
            raise Exception("Error: Product not found")
        product_stock = rows[0][0]
        return product_stock
    
    @staticmethod
    def get_cart_for_user(uid):
        items = CartDAL.get_items(uid)
        total_price = 0
        for item in items:
            total_price += item['quantity'] * item['at_price']
        return items, total_price
    
    @staticmethod
    def get_paginated_carts_by_user(uid, page, items_per_page):
        items = CartDAL.get_paginated_carts_by_user(uid, page, items_per_page)
        
        all_items = CartDAL.get_items(uid)
        total_price = 0
        for i in all_items:
            total_price += i['quantity'] * i['at_price']

        total_items = CartDAL.count_items_in_cart(uid)
        total_pages = (total_items + items_per_page - 1) // items_per_page
        return items, total_price, total_pages

    @staticmethod
    def add_item_to_cart(uid, product_id):
        product_stock = CartManager.check_product_stock(product_id)
        if product_stock <= 0:
            raise Exception("Out of Stock :(")
        return CartDAL.add_item(uid, product_id)

    @staticmethod
    def delete_item_from_cart(uid, product_id):
        return CartDAL.remove_item_from_cart(uid, product_id)

    @staticmethod
    def decrease_quantity(uid, product_id):
        new_quantity = CartDAL.decrease_quantity_of_item(uid, product_id)
        return new_quantity

    @staticmethod
    def clear_cart(uid):
        return CartDAL.clear_cart(uid)
    
    @staticmethod
    def place_order(uid):
        cart_items, total_price = CartManager.get_cart_for_user(uid)

        for item in cart_items:
            stock_quantity = CartManager.check_product_stock(item['product_id'])
            if stock_quantity < item['quantity']:
                return{
                    "success": False,
                    "error": f"Insufficient stock for product {item['product_name']}"
            }
                #  raise Exception(f"Insufficient stock for product {item['product_name']}")

        user_balance = CartManager.check_user_balance(uid)
        if user_balance < total_price:
            return {
            "success": False,
            "error": "Insufficient funds."
            }

        return CartDAL.place_order(total_price, uid)
