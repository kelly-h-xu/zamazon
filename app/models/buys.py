# IMPORTS
from flask import current_app as app

class Buys: 
    # INIT: Initialize a Buys object
    def __init__(self, buyer_id, purchase_id, at_balance):
        self.buyer_id = buyer_id
        self.purchase_id = purchase_id
        self.at_balance = at_balance
    
    # ____________
    # METHOD
    # TO_DICT: Convert the object to a dictionary
    def to_dict(self):
        return {
            "buyer_id": self.buyer_id,
            "purchase_id": self.purchase_id,
            "at_balance": self.at_balance
        }

    # Specific record by buyer and purchase id 
    @staticmethod
    def get_buys(buyer_id, purchase_id):
        # Query to grab the record that matches the buyer and purchase id
        rows = app.db.execute('''
        SELECT *
        FROM Buys
        WHERE buyer_id = :buyer_id AND purchase_id = :purchase_id
        ''',
        buyer_id=buyer_id, purchase_id=purchase_id)

        # Return the query output
        return Buys(*(rows[0])) if rows else None

    # All records in the Buys table 
    @staticmethod
    def get_all_buys():
        # Query to select all records in the Buys table
        rows = app.db.execute('''
        SELECT *
        FROM Buys
        ''')

        # Return the query output 
        return [Buys(*row) for row in rows]
    
    # ____________
    # METHOD
    # Endpoint for social.py
    # Check if user has purchased the product and if any of the orders are fulfilled (able to write review)
    def count_fulfilled_purchases_of_product(product_name, user_id):
        rows = app.db.execute('''
        SELECT COUNT(*) 
        FROM Orders o
        JOIN OrderContains oc ON o.purchase_id = oc.purchase_id
        JOIN Buys b ON b.purchase_id = o.purchase_id
        JOIN ProductListing pl ON oc.product_id = pl.product_id
        JOIN ProductCatalog p ON pl.product_name = p.product_name
        WHERE b.buyer_id = :user_id
        AND p.product_name = :product_name
        AND o.fulfillment_status = true;
        ''', product_name = product_name, user_id = user_id)
        return rows[0][0] if rows else 0
    
    # ____________
    # METHOD
    # Endpoint for social.py
    # Check if user has purchased the product from that seller and if any of the orders are fulfilled (able to write review)
    def count_fulfilled_purchases_of_seller_products(seller_id, user_id):
        rows = app.db.execute('''
        SELECT COUNT(*) 
        FROM Orders o
        JOIN OrderContains oc ON o.purchase_id = oc.purchase_id
        JOIN Buys b ON b.purchase_id = o.purchase_id
        JOIN ProductListing pl ON oc.product_id = pl.product_id
        WHERE b.buyer_id = :user_id
        AND pl.seller_id = :seller_id
        AND o.fulfillment_status = true;
        ''', seller_id = seller_id, user_id = user_id)
        return rows[0][0] if rows else 0

    @staticmethod
    def get_paginated_orders_by_buyer(buyer_id, page, items_per_page, sort_by='date_time'):
        # Define a mapping for valid sort columns
        valid_sort_columns = {
            'date_time': 'Orders.date_time',
            'total_amount': 'Orders.cost',
            'number_of_items': 'COUNT(OrderContains.product_id)',
            'fulfillment_status': 'Orders.fulfillment_status'
        }

        # Validate sort_by parameter and set default if invalid
        sort_column = valid_sort_columns.get(sort_by, 'Orders.date_time')

        # Calculate the offset for pagination
        offset = (page - 1) * items_per_page

        # Execute the query with pagination and dynamic sorting
        query = f'''
            SELECT 
                Orders.purchase_id AS order_id,
                Orders.date_time AS purchase_date,
                Orders.cost AS total_amount,
                COUNT(OrderContains.product_id) AS number_of_items,
                Orders.fulfillment_status
            FROM Buys
                JOIN Orders ON Buys.purchase_id = Orders.purchase_id
                JOIN OrderContains ON Orders.purchase_id = OrderContains.purchase_id
            WHERE Buys.buyer_id = :buyer_id
            GROUP BY Orders.purchase_id, Orders.date_time, Orders.cost, Orders.fulfillment_status
            ORDER BY {sort_column} DESC
            LIMIT :items_per_page OFFSET :offset
        '''

        # Execute the query
        rows = app.db.execute(query, buyer_id=buyer_id, items_per_page=items_per_page, offset=offset)

        # Return the results in dictionary form
        return [
            {
                'order_id': row[0],
                'purchase_date': row[1],
                'total_amount': row[2],
                'number_of_items': row[3],
                'fulfillment_status': row[4]
            }
            for row in rows
        ]

    # ____________
    # METHOD
    # GET_TOTAL_ORDERS_BY_BUYER: Count the number of unique orders placed by a user
    @staticmethod
    def get_total_orders_by_buyer(buyer_id):
        # Count the distinct orders associated with a user
        rows = app.db.execute('''
            SELECT COUNT(DISTINCT Orders.purchase_id)
            FROM Buys
            JOIN Orders ON Buys.purchase_id = Orders.purchase_id
            WHERE Buys.buyer_id = :buyer_id
        ''', buyer_id=buyer_id)
        
        # Extract the count from the result and return it
        total_orders = rows[0][0] if rows else 0
        return total_orders

    # ____________
    # METHOD
    # GET_BUYS_BY_ORDER: Get the products in one specified order
    @staticmethod
    def get_buys_by_order(purchase_id):
        # Query to select desired variables (product details and overview information)
        # from the Users, Buys, Orders, OrderContains, ProductListing, ProductCatalog
        # SellerReview, and ProductReview tables
        rows = app.db.execute('''
            SELECT 
                Users.user_id AS buyer_id,
                Buys.purchase_id,
                ProductListing.product_id,
                ProductListing.product_name,
                OrderContains.quantity,
                OrderContains.at_price AS price_at_purchase,
                Orders.date_time AS purchase_date,
                ProductReview.rating AS product_rating,
                ProductReview.comment AS product_comment,
                SellerReview.rating AS seller_rating,
                SellerReview.comment AS seller_comment,
                SellerUsers.user_id AS seller_id,
                SellerUsers.firstname AS seller_firstname,
                SellerUsers.lastname AS seller_lastname, 
                Buys.at_balance AS total_order_price,
                OrderContains.fulfillment_time,
                Orders.fulfillment_status,
                ProductCatalog.image_url,
                ProductCatalog.description
            FROM Buys
                JOIN Users ON Buys.buyer_id = Users.user_id
                JOIN Orders ON Buys.purchase_id = Orders.purchase_id
                JOIN OrderContains ON Orders.purchase_id = OrderContains.purchase_id
                JOIN ProductListing ON OrderContains.product_id = ProductListing.product_id
                JOIN ProductCatalog ON ProductListing.product_name = ProductCatalog.product_name
                LEFT JOIN ProductReview ON ProductReview.product_name = ProductListing.product_name
                    AND ProductReview.buyer_id = Users.user_id
                LEFT JOIN SellerReview ON SellerReview.seller_id = ProductListing.seller_id
                    AND SellerReview.buyer_id = Users.user_id
                JOIN Users AS SellerUsers ON ProductListing.seller_id = SellerUsers.user_id
            WHERE Buys.purchase_id = :purchase_id
            ORDER BY Orders.date_time DESC;
        ''', purchase_id= purchase_id)

        # Build a list of purchase records with product details and review info
        purchases = []
        for row in rows:
            purchase_details = {
                'user_id': row[0],
                'purchase_id': row[1],
                'at_balance': row[14],
                'fulfillment_time': row[15],
                'fulfillment_status': row[16],
                'product_id': row[2],
                'product_name': row[3],
                'quantity': row[4],
                'price_at_purchase': row[5],
                'purchase_date': row[6],
                'seller_id' : row[11],
                'seller_name': f"{row[12]} {row[13]}",
                'image_url': row[18] 
            }
            purchases.append(purchase_details)

        # Return the purchase list
        return purchases

        