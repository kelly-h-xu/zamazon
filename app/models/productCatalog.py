from flask import current_app as app
class ProductCatalog:
   DEFAULT_GET_QUERY = '''
               WITH MinPrices AS (
                   SELECT product_name, MIN(price) AS min_price
                   FROM ProductListing
                   GROUP BY product_name
               )
               SELECT p.product_id, p.product_name, p.price, category, image_url, description,
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


               JOIN MinPrices mp ON mp.product_name = p.product_name AND mp.min_price = p.price


               '''
   def __init__(self, product_id, product_name, min_price, category, description, image_url, total_reviews=0, avg_rating=0, total_purchases=0):
       self.product_id = product_id
       self.product_name = product_name
       self.min_price = min_price
       self.category = category
       self.description = description
       self.image_url = image_url
       self.total_reviews = total_reviews
       self.avg_rating = avg_rating
       self.total_purchases = total_purchases

   def get_product_by_name(product_name):
       query = ProductCatalog.DEFAULT_GET_QUERY
       query += " WHERE p.product_name = :product_name;"
       rows = app.db.execute(query, product_name=product_name)
       return [ProductCatalog(*rows[0]) for row in rows]
       
   '''
   for Product display page:
   get products by category (all, flowers, succulents, herbs, fruits and vegetables), their total reviews, their average ratings, and their total sales.
   accounts for filtering.  
   '''
   def get_products_by_category(category, search_term=None, column=None, order_by=None, limit=0, offset = 0):
       query = ProductCatalog.DEFAULT_GET_QUERY
       if search_term:
           search_term = f"%{search_term.lower()}%"
       if category != "all":
           query += f" WHERE category = :cat"
           if search_term:
            query += f" AND (LOWER(p.product_name) LIKE :search_term OR LOWER(description) LIKE :search_term)"
       else:
           if search_term:
               query += f" WHERE (LOWER(p.product_name) LIKE :search_term OR LOWER(description) LIKE :search_term)"
       if column and order_by:
           query += f" ORDER BY {column} {order_by}"
       query += f" LIMIT :lim"
       query += f" OFFSET :offset;"
       rows = app.db.execute(query, cat = category, search_term = search_term, lim=limit, offset=offset)
       return [ProductCatalog(*row) for row in rows]

  
   def get_total_products(category, search_term = None):
       query = f"SELECT COUNT(*) FROM ({ProductCatalog.DEFAULT_GET_QUERY}) AS total_count"
       if category != "all":
           query += f" WHERE category = :cat"
       if search_term:
           if category != "all":
               query += " AND (LOWER(product_name) LIKE :search_term OR LOWER(description) LIKE :search_term)"
           else:
               query += " WHERE (LOWER(product_name) LIKE :search_term OR LOWER(description) LIKE :search_term)"
           search_term = f"%{search_term.lower()}%"
       query += ";"
       rows = app.db.execute(query, cat = category, search_term=search_term)
       total = rows[0][0] if rows else 0
       return total