from flask import current_app as app
from app.models.product import Product
from datetime import datetime

class OrderInfo:

    def __init__(self, product_id, order_quantity, at_price, fulfillment_time,
                 name, price, category, description, image_url, product_quantity, 
                 date_time, fulfillment_status, address, purchase_id):
        self.product_id = product_id
        self.order_quantity = order_quantity
        self.at_price = at_price
        self.fulfillment_time = fulfillment_time
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.image_url = image_url
        self.product_quantity = product_quantity
        self.date_time = date_time
        self.fulfillment_status = fulfillment_status
        self.address = address
        self.purchase_id = purchase_id

class Seller:
    # update quantity column in listing table
    @staticmethod
    def change_product_quantity(product_id, quantity):
        try:
            app.db.execute("""
            UPDATE ProductListing
            SET quantity = :quantity
            WHERE product_id = :product_id
        """, product_id=product_id, quantity=quantity)
            return True
        except Exception as e:
            print(f"Failed to update item: {e}")
            return False
    
    # update price column in listing table
    @staticmethod
    def change_product_price(product_id, price):
        try:
            app.db.execute("""
            UPDATE ProductListing
            SET price = :price
            WHERE product_id = :product_id
        """, product_id=product_id, price=price)
            return True
        except Exception as e:
            print(f"Failed to update item: {e}")
            return False
    
    # check if user is in the sellers table
    @staticmethod
    def is_seller(seller_id):
        try:
            rows = app.db.execute('''
            SELECT * FROM Sellers WHERE seller_id = :seller_id
            ''', seller_id=seller_id)
            return len(rows)
        except Exception as e:
            print(f"Seller lookup failed: {e}")
            return False

    # update OrderContains table and update overall fulfillment status if needed
    @staticmethod
    def fulfill_order_item(purchase_id, product_id):
        try:
            app.db.execute('BEGIN')
            # Mark specific items as fulfilled
            current_time = datetime.now()
            app.db.execute('''
            UPDATE OrderContains
            SET fulfillment_time = :current_time
            WHERE purchase_id = :purchase_id AND product_id = :product_id
            ''', product_id=product_id, purchase_id=purchase_id, current_time=current_time)

            # if all items in the order are fulfilled
            rows = app.db.execute('''
            SELECT COUNT(*)
            FROM OrderContains
            WHERE purchase_id = :purchase_id AND fulfillment_time IS NULL
            ''', purchase_id=purchase_id)

            unfulfilled_count = rows[0][0]

            # Update the Orders table if all orders are fulfilled
            if unfulfilled_count == 0:
                app.db.execute('''
                UPDATE Orders
                SET fulfillment_status = true
                WHERE purchase_id = :purchase_id
                ''', purchase_id=purchase_id)

            app.db.execute('COMMIT')
            return True
        except Exception as e:
            app.db.execute('ROLLBACK')
            print(f"Failed to fulfill order item: {e}")
            return False

    # update columns of product catalog table
    @staticmethod
    def update_product_catlog(name, category, description, image_url):
        try:
            app.db.execute('''
            UPDATE ProductCatalog 
            SET category=:category, description=:description, image_url=:image_url
            WHERE product_name = :name
            ''',
            name=name,category=category,description=description,image_url=image_url)
            return True
        except Exception as e:
            print(f"Failed to add product: {e}")
            return False
        
    # add a seller to the sellers table
    @staticmethod
    def add_seller(seller_id):
        try:
            rows = app.db.execute('''
            INSERT INTO Sellers(seller_id)
            VALUES(:seller_id)''', seller_id=seller_id)
            return True
        except Exception as e:
            print(f"Failed to add seller: {e}")
    
    # get catalog information for product of given name, empty if name is available
    @staticmethod
    def verify_name_availability(product_name):
        try:
            rows = app.db.execute('''
                           SELECT image_url, description, category
                           FROM ProductCatalog
                           WHERE product_name=:product_name
                           ''', product_name=product_name)
            if len(rows) == 0: 
                return {}
            else: 
                ret = {'description': rows[0][0]}
                ret['image_url'] = rows[0][1]
                ret['category'] = rows[0][2]
                return ret
        except Exception as e:
            print(f"Failed to find name availability: {e}")
    
    # check if seller has item of same name in inventory to avoid duplicate listings
    @staticmethod
    def check_if_already_sold(product_name, seller_id):
        try:
            rows = app.db.execute('''
                           SELECT *
                           FROM ProductListing
                           WHERE product_name=:product_name AND seller_id=:seller_id
                           ''', product_name=product_name, seller_id=seller_id)
            if len(rows) == 0: 
                return False
            else: 
                return True
        except Exception as e:
            print(f"Failed to find name availability: {e}")

    # add new product to inventory
    @staticmethod
    def add_product_to_catalog(product_name, category, image_url, description, creator_id):
        try:
            seller_status = Seller.is_seller(creator_id)
            if not seller_status:
                Seller.add_seller(creator_id)
            app.db.execute('''
            INSERT INTO ProductCatalog(product_name, category, image_url, description, creator_id)
            VALUES(:product_name, :category, :image_url, :description, :creator_id)''',
            product_name=product_name, category=category, image_url=image_url, description=description, creator_id=creator_id)
            return True
        except Exception as e:
            print(f"Failed to add product: {e}")
            return False
    
    # set listing as inactive (preserves it in ordercontains table)
    @staticmethod
    def remove_listing(product_id):
        try:
            app.db.execute('''
            UPDATE ProductListing
            SET active = false
            WHERE product_id =:product_id
            ''', product_id=product_id)
            return True
        except Exception as e:
            print(f"Failed to delete product: {e}")
            return False

    # add listing of existing product, if already sold by this seller, update quantity/price
    # else, add new row to table
    @staticmethod
    def add_product_listing(product_name, seller_id, price, quantity):
       try:
            if (Seller.check_if_already_sold(product_name, seller_id)):
                app.db.execute('''
                               UPDATE ProductListing
                               SET price=:price, quantity=:quantity
                               WHERE product_name=:product_name AND seller_id=:seller_id
                               ''', price=price, quantity=quantity, product_name=product_name, seller_id=seller_id)
                return True
            app.db.execute('''
            INSERT INTO ProductListing(product_name, seller_id, price, quantity)
            VALUES(:product_name, :seller_id, :price, :quantity)''',
            product_name=product_name, seller_id=seller_id, price=price, quantity=quantity)
            return True
       except Exception as e:
            print(f"Failed to add product: {e}")
            return False
    
    # get items that are fulfilled (has a fulfillment time)
    @staticmethod
    def get_fulfilled_ordered_items_by_seller(seller_id, page, items_per_page):
        offset = (page - 1) * items_per_page
        rows = app.db.execute('''
        SELECT ProductListing.product_id, OrderContains.quantity as order_quantity, at_price, fulfillment_time,
            product_name, price, category, image_url, description, ProductListing.quantity as product_quantity,
            Orders.date_time, fulfillment_status,
            address, purchase_id
        FROM OrderContains 
        JOIN ProductListing ON ProductListing.product_id=OrderContains.product_id
        NATURAL JOIN ProductCatalog
        NATURAL JOIN Orders
        NATURAL JOIN Buys
        JOIN Users ON buyer_id=user_id
        WHERE seller_id = :seller_id AND fulfillment_time IS NOT NULL
        ORDER BY fulfillment_time DESC, date_time DESC
        LIMIT :page_size OFFSET :offset
        ''',seller_id=seller_id, page_size=items_per_page, offset=offset)
        ret = [OrderInfo(*row) for row in rows]

        total = app.db.execute('''SELECT COUNT(*) 
        FROM OrderContains 
        JOIN ProductListing ON ProductListing.product_id = OrderContains.product_id
        NATURAL JOIN ProductCatalog
        NATURAL JOIN Orders
        NATURAL JOIN Buys
        JOIN Users ON buyer_id = user_id
        WHERE seller_id = :seller_id 
        AND fulfillment_time IS NULL''', seller_id=seller_id)

        return ret, total[0][0]
    
    # get items that are unfulfilled (have no listed fulfillment time)
    @staticmethod
    def get_unfulfilled_ordered_items_by_seller(seller_id, page, items_per_page):
        offset = (page - 1) * items_per_page
        rows = app.db.execute('''
        SELECT ProductListing.product_id, OrderContains.quantity as order_quantity, at_price, fulfillment_time,
            product_name, price, category, image_url, description, ProductListing.quantity as product_quantity,
            Orders.date_time, fulfillment_status,
            address, purchase_id
        FROM OrderContains 
        JOIN ProductListing ON ProductListing.product_id=OrderContains.product_id
        NATURAL JOIN ProductCatalog
        NATURAL JOIN Orders
        NATURAL JOIN Buys
        JOIN Users ON buyer_id=user_id
        WHERE seller_id = :seller_id AND fulfillment_time IS NULL
        ORDER BY date_time DESC
        LIMIT :page_size OFFSET :offset
        ''',seller_id=seller_id, page_size=items_per_page, offset=offset)
        ret = [OrderInfo(*row) for row in rows]

        total = app.db.execute('''SELECT COUNT(*) 
        FROM OrderContains 
        JOIN ProductListing ON ProductListing.product_id = OrderContains.product_id
        NATURAL JOIN ProductCatalog
        NATURAL JOIN Orders
        NATURAL JOIN Buys
        JOIN Users ON buyer_id = user_id
        WHERE seller_id = :seller_id 
        AND fulfillment_time IS NULL''', seller_id=seller_id)

        return ret, total[0][0]
    
    # get all products w/ pagination for frontend display
    @staticmethod
    def get_paginated_products_by_seller(seller_id, page, items_per_page):
        offset = (page - 1) * items_per_page
        rows = app.db.execute('''
        SELECT p.product_id, p.product_name, p.seller_id, p.price, p.quantity, c.category, c.image_url, c.description, c.creator_id
        FROM ProductListing p
        JOIN ProductCatalog c ON p.product_name = c.product_name
        WHERE p.seller_id = :seller_id AND active = true
        ORDER BY p.product_id
        LIMIT :page_size OFFSET :offset
        ''', seller_id=seller_id, page_size=items_per_page, offset=offset)

        total_count_row = app.db.execute('''
        SELECT COUNT(*)
        FROM ProductListing p
        WHERE p.seller_id = :seller_id AND active = true
        ''', seller_id=seller_id)
        total_count = total_count_row[0][0] if total_count_row else 0

        return [Product(*row) for row in rows], total_count

    # get products for a seller w/o pagination
    @staticmethod
    def get_products_by_seller(seller_id):
        rows = app.db.execute('''
        SELECT p.product_id, p.product_name, seller_id, price, quantity, category, image_url,
                description, creator_id, 
                COALESCE(pr.total_reviews, 0) AS total_reviews,
                COALESCE(pr.average_rating, 0) AS avg_rating,
                COALESCE(o.total_purchases, 0) AS total_purchases

        FROM ProductListing p

        NATURAL JOIN ProductCatalog

        LEFT JOIN (
            SELECT product_name,
                   COUNT(rating) AS total_reviews,
                   ROUND(AVG(rating), 1) AS average_rating
            FROM ProductReview
            GROUP BY product_name
        ) pr ON p.product_name = pr.product_name

        LEFT JOIN (
            SELECT product_id,
                   COUNT(product_id) AS total_purchases
            FROM OrderContains
            GROUP BY product_id
        ) o ON p.product_id = o.product_id

        WHERE p.seller_id = :seller_id AND active = true

        ''', seller_id=seller_id)
        return [Product(*row) for row in rows]