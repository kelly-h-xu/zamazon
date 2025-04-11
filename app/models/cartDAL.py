from flask import current_app as app

# CartDAL
class CartDAL:
    # managing individual cart items and item level logic like quantities and prices
    def __init__(self, uid, product_id, quantity, at_price):
        self.uid = uid
        self.product_id = product_id
        self.quantity = quantity
        self.at_price = at_price

    @staticmethod
    def get_product_stock(product_id):
        # how many items are present in stock for a particular product
        rows = app.db.execute ('''
            SELECT quantity
            FROM ProductListing 
            WHERE product_id = :product_id
        ''', product_id = product_id)
        return rows
        
    @staticmethod
    def get_user_balance(uid):
        # Check the money the user has in their account 
        rows = app.db.execute ('''
        SELECT balance
        FROM Users
        WHERE user_id = :uid
        ''', uid = uid)
        return rows

    @staticmethod
    def get_paginated_carts_by_user(uid, page, items_per_page):
        offset = (page - 1) * items_per_page 
        rows = app.db.execute ('''
        WITH Pdeets AS
        (
        SELECT pc.image_url, pl.product_name, pc.description
        FROM ProductCatalog pc
        JOIN ProductListing pl ON pl.product_name = pc.product_name
        ) 
        SELECT DISTINCT pl.product_id, pl.product_name, cc.quantity, cc.at_price, pd.description, pl.seller_id, pd.image_url
        FROM ProductListing pl
        JOIN Pdeets pd ON pd.product_name = pl.product_name
        JOIN CartContains cc ON cc.product_id = pl.product_id
        WHERE cc.uid = :uid 
        ORDER BY pl.product_id ASC
        LIMIT :items_per_page OFFSET :offset
        ''', uid=uid, items_per_page = items_per_page, offset = offset)
        items = []
        for row in rows:
            item = {
                'product_id' : row [0],
                'product_name': row[1],
                'quantity': row[2],
                'at_price': row[3], 
                'image_url': row[4], 
                'seller_id': row[5]
            }
            items.append(item)
        return items

    @staticmethod
    def count_items_in_cart(uid):
        result = app.db.execute('''
        SELECT COUNT(*)
        FROM CartContains
        WHERE uid = :uid
        ''', uid=uid)
        return result[0][0] if result else 0

    @staticmethod
    def get_items(uid) :
        # Similar code to the one above but to make it easier for backend methods as seen down below as well.
        rows = app.db.execute ('''
        WITH Pdeets AS
        (
        SELECT pc.image_url, pl.product_name, pc.description
        FROM ProductCatalog pc
        JOIN ProductListing pl ON pl.product_name = pc.product_name
        ) 
        SELECT DISTINCT pl.product_id, pl.product_name, cc.quantity, cc.at_price, pd.description, pl.seller_id, pd.image_url
        FROM ProductListing pl
        JOIN Pdeets pd ON pd.product_name = pl.product_name
        JOIN CartContains cc ON cc.product_id = pl.product_id
        WHERE cc.uid = :uid 
        ''', uid=uid)
        items = []
        for row in rows:
            item = {
                'product_id' : row [0],
                'product_name': row[1],
                'quantity': row[2],
                'at_price': row[3], 
                'image_url': row[4], 
                'seller_id': row[5]
            }
            items.append(item)
        return items
    
    @staticmethod
    def add_item(uid, product_id) -> bool:
        # Increases quantity of item if it already exists
        # If item does not exist in cart, add item. 
        try:
            rows = app.db.execute('''
            INSERT INTO CartContains (uid ,product_id, quantity, at_price)
            VALUES(
            :uid, 
            :product_id, 
            1, 
            (SELECT p.price FROM ProductListing p WHERE p.product_id=:product_id))
            ON CONFLICT(uid, product_id)
            DO UPDATE SET quantity = GREATEST(1, CartContains.quantity + 1);
            ''', 
            uid = uid, product_id = product_id)
            return True
        except Exception as e:
            print(f"Failed to add item: {e}")
            return False
        
    @staticmethod
    def remove_item_from_cart(uid, product_id) -> bool:
        # Remove an item from the cart of a user
        try:
            rows = app.db.execute('''
            DELETE 
            FROM CartContains cc
            WHERE cc.uid = :uid AND cc.product_id = :product_id
            ''', uid= uid, product_id = product_id)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False
        
    @staticmethod
    def decrease_quantity_of_item(uid, product_id) -> int:
        # Decrease the quantity of an item by 1
        # Basically like the minus sign in the cart
        try:
            rows = app.db.execute('''
            UPDATE CartContains cc
            SET quantity = CASE
                    WHEN cc.quantity > 1 THEN cc.quantity - 1
                    ELSE cc.quantity
            END
            WHERE cc.uid = :uid AND cc.product_id = :product_id 
            RETURNING cc.quantity
            ''', uid= uid, product_id = product_id)
            print(rows)
            return rows[0][0]
        except Exception as e:
            print(f"Failed: {e}")
    
    @staticmethod
    def clear_cart(uid) -> bool:
        # Clears the cart of a user
        try:
            rows = app.db.execute('''
            DELETE
            FROM CartContains cc
            WHERE cc.uid = :uid
            ''', uid=uid)
            return True
        except Exception as e:
            print(f"Failed to clear cart: {e}")
            return False
    @staticmethod
    def sync_order_sequence():
        try:
            app.db.execute('''
                SELECT setval('orders_purchase_id_seq', (SELECT COALESCE(MAX(purchase_id), 0) FROM Orders));
            ''')
        except Exception as e:
            print(f"Failed to sync order sequence: {e}")
            raise


    @staticmethod
    def place_order(cost,uid):
        try:
            CartDAL.sync_order_sequence()
            app.db.execute("BEGIN")
            print("Transaction started.")

            # Create an entry in the orders table
            rows = app.db.execute('''
                INSERT INTO Orders (cost)
                VALUES (:cost)
                RETURNING purchase_id, date_time
            ''', cost=cost)
            purchase_id, date_time = rows[0]
            print(f"Order created: purchase_id={purchase_id}, date_time={date_time}")

            cart_items = CartDAL.get_items(uid)
            # print(f"Cart items retrieved: {cart_items}")

            # insert entries to the OrderContains table
            for item in cart_items:
                app.db.execute('''
                    INSERT INTO OrderContains (purchase_id, product_id, quantity, at_price)
                    VALUES (:purchase_id, :product_id, :quantity, :at_price)
                ''', purchase_id=purchase_id, product_id=item['product_id'], quantity=item['quantity'], at_price=item['at_price'])
                print(f"Inserted into OrderContains for product_id={item['product_id']}")

            # Update the quantity of the product
            for item in cart_items: 
                app.db.execute('''
                    UPDATE ProductListing 
                    SET quantity = quantity - :quantity
                    WHERE product_id = :product_id;
                ''', product_id = item['product_id'], quantity = item['quantity'])
                print(f"Updated ProductListing quantity for product_id={item['product_id']}")

            # Subtract the total cost from balance of the user
            app.db.execute('''
                UPDATE Users
                SET balance = balance - :cost
                WHERE user_id = :uid
            ''', cost = cost, uid= uid)
            print(f"Updated user balance for uid={uid}")

            # Update seller balances
            for item in cart_items:
                print(f"Updating seller balance: product_id={item['product_id']}, seller_id={item['seller_id']}, at_price={item['at_price']}, quantity={item['quantity']}")
                app.db.execute('''
                    UPDATE Users
                    SET balance = balance + (:at_price * :quantity)
                    WHERE user_id = (SELECT seller_id FROM ProductListing WHERE product_id = :product_id)
                ''', at_price = item['at_price'], quantity = item['quantity'], product_id = item['product_id'])
                print(f"Updated seller balance {item['seller_id']} for product_id={item['product_id']}")
            
            # Insert purchase to Buys
            app.db.execute('''
            INSERT INTO Buys (buyer_id, purchase_id, at_balance)
            VALUES (:buyer_id, :purchase_id, :at_balance)
        ''', buyer_id=uid, purchase_id=purchase_id, at_balance=(cost * -1))  # at_balance tracks the cost
            print(f"Inserted into Buys: buyer_id={uid}, purchase_id={purchase_id}, totcost={cost}")

    #    Clear cart after submission of an order
            CartDAL.clear_cart(uid)
            print(f"Cleared cart for uid={uid}")

            app.db.execute("COMMIT")
            print("Transaction committed successfully.")

            return {
            "success": True,
            "message": "Order placed successfully.",
            "purchase_id": purchase_id,
            "date_time": date_time
        }
        except Exception as e:
            app.db.execute("ROLLBACK")
            print("Transaction failed:", e)
            return {
            "success": False,
            "message": str(e)}
            
    @staticmethod
    # just a dummy function to test order submission and changes of the user's balance.
    def update_balance(uid):
        rows = app.db.execute('''
        UPDATE Users 
        SET balance = balance + 100
        WHERE user_id = :uid
        ''', uid = uid)
        return True
