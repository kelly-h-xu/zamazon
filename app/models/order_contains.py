from flask import current_app as app

# CREATE TABLE OrderContains (
#     purchase_id INT NOT NULL REFERENCES Order(purchase_id),
#     product_id INT NOT NULL REFERENCES Product(product_id),
#     quantity INT NOT NULL,
#     at_price INT NOT NULL,
#     fulfillment_time TIMESTAMP SET TIME ZONE TO UTC,
#     PRIMARY KEY(purchase_id, product_id)
# );

class OrderContainsDAL:
    def __init__(self, purchase_id, product_id, quantity, at_price, fulfillment_time = None):
        self.purchase_id = purchase_id
        self.product_id = product_id
        self.quantity = quantity
        self.at_price = at_price
        self.fulfillment_time = fulfillment_time

    @staticmethod
    def get_products_by_order(purchase_id):
        rows = app.db.execute('''
        SELECT *
        FROM OrderContains
        WHERE purchase_id = :purchase_id''',
        purchase_id=purchase_id)
        return OrderContains(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def get_unfillfilled_items_by_order(purchase_id):
        rows = app.db.execute('''
        SELECT *
        FROM OrderContains
        WHERE purchase_id = :purchase_id AND fulfillment_time IS NULL
        ''', purchase_id=purchase_id)
        return [OrderContains(*row) for row in rows]

    @staticmethod
    def get_all_ordered_items():
        rows = app.db.execute('''
        SELECT *
        FROM OrderContains
        ''')
        return [OrderContains(*row) for row in rows]

    @staticmethod
    def add_order_item(purchase_id, product_id, quantity, at_price):
        try:
            rows = app.db.execute('''
            BEGIN TRANSACTION;
            SELECT p.quantity FROM Product p WHERE p.product_id =: product_id

            INSERT INTO OrderContains (purchase_id, product_id, quantity, at_price)
            VALUES (:purchase_id, :product_id, :quantity, :at_price)

            UPDATE Product p
            SET p.quantity = p.quantity - :quantity
            WHERE p.product_id = :product_id;

            COMMIT;

            ''', purchase_id=purchase_id, product_id= product_id, quantity = quantity, at_price = at_price)
            return True
        except Exception as e:
            print(f"Failed to submit order: {e}")
            return False

        
