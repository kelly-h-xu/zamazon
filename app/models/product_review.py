from flask import current_app as app
from datetime import datetime

class ProductReview:
    def __init__(self, buyer_id, product_name, rating, comment, date_time, upvote_count=None):
        self.buyer_id = buyer_id
        self.product_name = product_name
        self.rating = rating
        self.comment = comment
        self.date_time = date_time
        self.upvote_count = upvote_count
        
    @staticmethod
    # Get the review for a specific product by a specific buyer, along with the product name
    # Use the ProductCatalog since that is that product (can be sold in diff listings by diff sellers)
    def get_product_review(buyer_id, product_name):
        rows = app.db.execute('''
        SELECT pr.buyer_id, pr.product_name, pr.rating, pr.comment, pr.date_time
        FROM ProductReview pr
        JOIN ProductCatalog p ON pr.product_name = p.product_name
        WHERE pr.buyer_id = :buyer_id AND pr.product_name = :product_name
        ''', buyer_id=buyer_id, product_name=product_name)
        
        return ProductReview(*(rows[0])) if rows else None
    
    @staticmethod
    # Get all product reviews by a buyer
    def get_product_reviews_by_buyer(buyer_id):
        rows = app.db.execute('''
        SELECT pr.buyer_id, pr.product_name, pr.rating, pr.comment, pr.date_time
        FROM ProductReview pr
        JOIN ProductCatalog p ON pr.product_name = p.product_name
        WHERE pr.buyer_id = :buyer_id
        ''', buyer_id=buyer_id)
        return [ProductReview(*row) for row in rows] if rows else []

    ## PRODUCT DETAIL PAGE QUERIES ##
    
    @staticmethod
    # Get PAGINATED and SORTED reviews for a product by name -- for ProductDetail page
    def get_paginated_reviews_for_product_by_name(product_name, page, items_per_page, sort_by):
        offset = (page - 1) * items_per_page  # Calculate the offset for pagination
        
        # Separate into 2 cases: 
        # 1) the upvote count special case for top 3 most helpful and then by most recent sorting
        # 2) standard sorting options

        if sort_by == "top_helpful_recent":
            # top 3 most helpful reviews
            # need to do groupby for aggregate query use!!
            top_helpful_reviews = app.db.execute('''
                SELECT pr.buyer_id, u.firstname, u.lastname, pr.product_name, pr.rating, pr.comment, pr.date_time, COUNT(pru.voter_id) AS upvote_count
                FROM ProductReview pr
                JOIN Users u ON pr.buyer_id = u.user_id
                LEFT JOIN ProductReviewUpvote pru ON pr.buyer_id = pru.buyer_id AND pr.product_name = pru.product_name
                WHERE pr.product_name = :product_name
                GROUP BY pr.buyer_id, u.firstname, u.lastname, pr.product_name, pr.rating, pr.comment, pr.date_time
                ORDER BY upvote_count DESC
                LIMIT 3
            ''', product_name=product_name)

            # use buyer_id, product_id to filter out the queries we need
            top_helpful_ids = [(row[0], row[3]) for row in top_helpful_reviews]

            # get rest of reviews by time
            all_recent_reviews = app.db.execute('''
                SELECT pr.buyer_id, u.firstname, u.lastname, pr.product_name, pr.rating, pr.comment, pr.date_time, COUNT(pru.voter_id) AS upvote_count
                FROM ProductReview pr
                JOIN Users u 
                ON pr.buyer_id = u.user_id
                LEFT JOIN ProductReviewUpvote pru 
                ON pr.buyer_id = pru.buyer_id AND pr.product_name = pru.product_name
                WHERE pr.product_name = :product_name AND (pr.buyer_id, pr.product_name) NOT IN :top_helpful_ids
                GROUP BY pr.buyer_id, u.firstname, u.lastname, pr.product_name, pr.rating, pr.comment, pr.date_time
                ORDER BY pr.date_time DESC
            ''', product_name=product_name, top_helpful_ids=tuple(top_helpful_ids))

            # combo results for special sorting case
            combined_reviews = top_helpful_reviews + all_recent_reviews

            # paginate combined list
            paginated_combined_reviews = combined_reviews[offset : offset + items_per_page]

            return [
                {
                    'buyer_id': row[0],
                    'firstname': row[1],
                    'lastname': row[2],
                    'product_name': row[3],
                    'rating': row[4],
                    'comment': row[5],
                    'date_time': row[6],
                    'upvote_count': row[7]
                }
                for row in paginated_combined_reviews
            ]

        else:
            # all other sorting cases
            sort_column = {
                "helpful": "upvote_count DESC, pr.date_time DESC",
                "rating_high": "pr.rating DESC",
                "rating_low": "pr.rating ASC",
                "date_newest": "pr.date_time DESC",
                "date_oldest": "pr.date_time ASC"
            }.get(sort_by)

            rows = app.db.execute(f'''
                SELECT pr.buyer_id, u.firstname, u.lastname, pr.product_name, pr.rating, pr.comment, pr.date_time, COUNT(pru.voter_id) AS upvote_count
                FROM ProductReview pr
                JOIN Users u ON pr.buyer_id = u.user_id
                LEFT JOIN ProductReviewUpvote pru ON pr.buyer_id = pru.buyer_id AND pr.product_name = pru.product_name
                WHERE pr.product_name = :product_name
                GROUP BY pr.buyer_id, u.firstname, u.lastname, pr.product_name, pr.rating, pr.comment, pr.date_time
                ORDER BY {sort_column}
                LIMIT :items_per_page OFFSET :offset
            ''', product_name=product_name, items_per_page=items_per_page, offset=offset)

            return [
                {
                    'buyer_id': row[0],
                    'firstname': row[1],
                    'lastname': row[2],
                    'product_name': row[3],
                    'rating': row[4],
                    'comment': row[5],
                    'date_time': row[6],
                    'upvote_count': row[7]
                }
                for row in rows
            ]

    @staticmethod
    # Get total number of reviews for a specific product (by name) to calculate total pages on the frontend -- for ProductDetail page
    def count_reviews_for_product_by_name(product_name):
        rows = app.db.execute('''
        SELECT COUNT(*)
        FROM ProductReview pr
        WHERE pr.product_name = :product_name
        ''', product_name=product_name)
        return rows[0][0] if rows and rows[0][0] else 0
    
    @staticmethod
    # Get the product rating summary for a product -- for ProductDetailPage
    def get_product_rating_summary(product_name):
        rows = app.db.execute('''
        SELECT 
            AVG(pr.rating) AS average_rating,
            MIN(pr.rating) AS lowest_rating,
            MAX(pr.rating) AS highest_rating,
            COUNT(pr.rating) AS total_ratings
        FROM ProductReview pr
        WHERE pr.product_name = :product_name
        ''', product_name=product_name)
        
        return {
            'average_rating' : rows[0][0] if rows else None,
            'lowest_rating' : rows[0][1] if rows else None,
            'highest_rating' : rows[0][2] if rows else None,
            'total_ratings' : rows[0][3] if rows else None
        }

    ## CREATE, UPDATE, DELETE PRODUCT REVIEW ##

    @staticmethod
    # Write a new product review
    def new_product_review(product_name, buyer_id, rating, comment, date_time):
        try:
            rows = app.db.execute('''
            INSERT INTO ProductReview (product_name, buyer_id, rating, comment, date_time)
            VALUES (:product_name, :buyer_id, :rating, :comment, :date_time)
            ''', product_name=product_name, buyer_id=buyer_id, rating=rating, comment=comment, date_time=date_time)
            return True
        except Exception as e:
            print(f"Failed to write item: {e}")
            return False
    
    @staticmethod
    # Delete product review
    def delete_product_review(product_name, buyer_id):
        try:
            rows = app.db.execute('''
            DELETE 
            FROM ProductReview
            WHERE product_name = :product_name AND buyer_id = :buyer_id
            ''', product_name=product_name, buyer_id=buyer_id)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False
        
    @staticmethod
    # Edit product review
    def edit_product_review(product_name, buyer_id, rating, comment, date_time):
        try:
            rows = app.db.execute('''
                UPDATE ProductReview 
                SET rating = :rating, comment = :comment, date_time = :date_time
                WHERE product_name = :product_name AND buyer_id = :buyer_id
                ''', product_name=product_name, buyer_id=buyer_id, rating=rating, comment=comment, date_time=date_time)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False

    ## OLD ENDPOINT ## 
    
    @staticmethod
    # Get the most recent k product reviews authored by a specific user, along with product names
    def get_k_recent_product_reviews_by_user(uid, k):
        rows = app.db.execute('''
        SELECT pr.buyer_id, pr.product_name, pr.rating, pr.comment, pr.date_time
        FROM ProductReview pr
        JOIN ProductListing p ON pr.product_name = p.product_name
        WHERE pr.buyer_id = :uid
        ORDER BY pr.date_time DESC
        LIMIT :k
        ''', uid=uid, k=k)
        return [ProductReview(*row) for row in rows]
    
    ## SOCIAL CENTER IN USER ACCOUNTS ##
    
    @staticmethod
    # Get paginated product reviews authored by a specific user, along with product names
    def get_paginated_product_reviews_by_user(uid, page, items_per_page):
        offset = (page - 1) * items_per_page # calculate offset
        rows = app.db.execute('''
        SELECT pr.buyer_id, pr.product_name, pr.rating, pr.comment, pr.date_time
        FROM ProductReview pr
        JOIN ProductCatalog p ON pr.product_name = p.product_name
        WHERE pr.buyer_id = :uid
        ORDER BY pr.date_time DESC
        LIMIT :items_per_page OFFSET :offset
        ''', uid=uid, items_per_page=items_per_page, offset=offset)
        return [ProductReview(*row) for row in rows]
    
    @staticmethod
    # Get total amount of product reviews by a user to calculate num pages on frontend
    # Can also use this to get a users review stats!
    def count_product_reviews_by_user(uid):
        rows = app.db.execute('''
        SELECT COUNT(*)
        FROM ProductReview
        WHERE buyer_id = :uid
        ''', uid=uid)
        return rows[0][0] if rows[0][0] else 0

    ## CONVERT TO DICT FUNCTIONALITY ##
    
    def to_dict(self):
        return {
            'buyer_id': self.buyer_id,
            'product_name': self.product_name,
            'rating': self.rating,
            'comment': self.comment,
            'date_time': self.date_time.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.date_time, datetime) else self.date_time, # format the date_time if it's a datetime object to a string for JSON serialization
            'upvote_count':self.upvote_count if self.upvote_count else 0
        }
