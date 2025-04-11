from flask import current_app as app
class ProductListing():
    def __init__(self, product_id, product_name, seller_id, price, quantity, active, seller_name):
       self.product_id = product_id
       self.product_name = product_name
       self.seller_id = seller_id
       self.price = price
       self.quantity = quantity
       self.active = active
       self.seller_name = seller_name
    
    @staticmethod
    def get_listing_by_name(product_name):
        query = '''
                SELECT pl.*, u.firstname || ' ' || u.lastname AS seller_name
                FROM ProductListing pl 
                JOIN Users u 
                on pl.seller_id = u.user_id
                WHERE product_name = :product_name
                '''
        rows = app.db.execute(query, product_name = product_name)
        return [ProductListing(*row) for row in rows]

