from flask import current_app as app


class Product:
   def __init__(self, product_id, product_name, seller_id, price, quantity, category, description, image_url, creator_id, total_reviews=0, avg_rating=0, total_purchases=0):
       self.product_id = product_id
       self.product_name = product_name
       self.price = price
       self.category = category
       self.description = description
       self.image_url = image_url
       self.seller_id = seller_id
       self.quantity = quantity
       self.total_reviews = total_reviews
       self.avg_rating = avg_rating
       self.total_purchases = total_purchases
       self.creator_id = creator_id
  
   def to_dict(self):
       return {
           "product_id": self.product_id,
           'product_name': self.product_name,
           "price": self.price,
           "quantity": self.quantity,
           "category": self.category,
           "description": self.description,
           "image_url": self.image_url
       }
      
   @staticmethod
   def get(product_id):
       rows = app.db.execute('''
                               SELECT product_id, product_name, seller_id, price, quantity,category, description,image_url, creator_id
                               FROM ProductListing
                               NATURAL JOIN ProductCatalog
                               WHERE product_id = :id
                               ''',
                             id=product_id)
       return Product(*(rows[0])) if rows is not None else None #return the product matching the id we gave
   
   @staticmethod
   def get_listing_by_name(product_name):
       query = '''
                SELECT product_id, product_name, seller_id, price, quantity, category, description, image_url, creator_id
                FROM ProductListing
                NATURAL JOIN ProductCatalog
                WHERE product_name = :product_name
                '''
       rows = app.db.execute(query, product_name = product_name)
       return [Product(*row) for row in rows]

   '''
   get all products, their total reviews, their average ratings, and their total sales.
   accounts for filtering.  
   '''
   @staticmethod
   def get_all(column=None, order_by=None, limit=0, offset = 0):
       query = '''
               SELECT p.product_id, p.product_name, seller_id, price, quantity, category, image_url, description, creator_id,
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
               '''
       if column and order_by:
           query += f"ORDER BY {column} {order_by}"
       query += f" LIMIT {limit}"
       query += f" OFFSET {offset};"
       rows = app.db.execute(query)
       return [Product(*row) for row in rows]
  
   @staticmethod
   def get_total_num_products():
       query = '''
               SELECT COUNT(*)
               FROM ProductListing
               '''
       total = app.db.execute(query)
       return total[0][0]