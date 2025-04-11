from flask import current_app as app
from datetime import datetime

class SellerReview:
    def __init__(self, buyer_id, seller_id, rating, comment, date_time, seller_firstname=None, seller_lastname=None):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.rating = rating
        self.comment = comment
        self.date_time = date_time # when the review was written
        
        self.seller_firstname = seller_firstname # include seller_firstname
        self.seller_lastname = seller_lastname # include seller_lastname

    @staticmethod
    # Get the review for a specific seller by a specific buyer
    def get_buyer_seller_review(buyer_id, seller_id):
        rows = app.db.execute('''
        SELECT buyer_id, seller_id, rating, comment, date_time
        FROM SellerReview
        WHERE buyer_id := buyer_id AND seller_id := seller_id
        ''', buyer_id=buyer_id, seller_id=seller_id)
        return SellerReview(*(rows[0])) if rows else None
    
    @staticmethod
    # Get all seller reviews by a buyer
    def get_seller_reviews_by_buyer(buyer_id):
        rows = app.db.execute('''
        SELECT buyer_id, seller_id, rating, comment, date_time
        FROM SellerReview sr
        WHERE buyer_id = :buyer_id
        ''', buyer_id=buyer_id)
        
        return [SellerReview(*row) for row in rows] if rows else []
    
    @staticmethod
    # Get all reviews for a specific seller
    def get_all_reviews_for_seller(seller_id):
        rows = app.db.execute('''
        SELECT buyer_id, seller_id, rating, comment, date_time
        FROM SellerReview
        WHERE seller_id = :seller_id
        ''', seller_id=seller_id)
        return [SellerReview(*row) for row in rows] if rows else []
    
        
    @staticmethod
    # Get the review for a specific seller by a specific buyer
    def get_seller_review(buyer_id, seller_id):
        rows = app.db.execute('''
        SELECT buyer_id, seller_id, rating, comment, date_time
        FROM SellerReview
        WHERE buyer_id = :buyer_id AND seller_id = :seller_id
        ''', buyer_id=buyer_id, seller_id=seller_id)
        return SellerReview(*(rows[0])) if rows else None
    

    @staticmethod
    # Each user should be able to list all ratings/reviews authored by this user, sorted in reverse chronological order by default
    def get_k_recent_seller_reviews_by_user(uid, k):
        rows = app.db.execute('''
        SELECT sr.buyer_id, sr.seller_id, sr.rating, sr.comment, sr.date_time, u.firstname AS seller_firstname, u.lastname AS seller_lastname
        FROM SellerReview sr 
        JOIN Users u ON sr.seller_id = u.user_id
        WHERE buyer_id = :uid
        ORDER BY date_time DESC
        LIMIT :k
        ''', uid=uid, k=k)
        print(rows)
        return [SellerReview(*row) for row in rows]
    
    @staticmethod
    # Get the overall/average rating for a specific seller
    def get_seller_review_summary(seller_id):
        rows = app.db.execute('''
        SELECT AVG(sr.rating) AS average_rating,
            MIN(sr.rating) AS lowest_rating,
            MAX(sr.rating) AS highest_rating,
            COUNT(sr.rating) AS total_ratings
        FROM SellerReview sr
        WHERE sr.seller_id = :seller_id
        ''', seller_id=seller_id)
        return {
            'average_rating' : rows[0][0] if rows else None,
            'lowest_rating' : rows[0][1] if rows else None,
            'highest_rating' : rows[0][2] if rows else None,
            'total_ratings' : rows[0][3] if rows else None
        }

    
    @staticmethod
    # Write a new seller review
    def new_seller_review(seller_id, buyer_id, rating, comment, date_time):
        try:
            rows = app.db.execute('''
            INSERT INTO SellerReview (seller_id, buyer_id, rating, comment, date_time)
            VALUES (:seller_id, :buyer_id, :rating, :comment, :date_time)
            ''', seller_id=seller_id, buyer_id=buyer_id, rating=rating, comment=comment, date_time=date_time)
            return True
        except Exception as e:
            print(f"Failed to write item: {e}")
            return False
        
    @staticmethod
    # Delete seller review
    def delete_seller_review(seller_id, buyer_id):
        try:
            rows = app.db.execute('''
                DELETE 
                FROM SellerReview
                WHERE seller_id = :seller_id AND buyer_id = :buyer_id
                ''', seller_id=seller_id, buyer_id=buyer_id)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False
        
    @staticmethod
    # Edit seller review
    def edit_seller_review(seller_id, buyer_id, rating, comment, date_time):
        try:
            rows = app.db.execute('''
                UPDATE SellerReview 
                SET rating = :rating, comment = :comment, date_time = :date_time
                WHERE seller_id = :seller_id AND buyer_id = :buyer_id
                ''', seller_id=seller_id, buyer_id=buyer_id, rating=rating, comment=comment, date_time=date_time)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False
    
    ## PAGINATED DISPLAY ALL SELLER REVIEWS BY A USER

    @staticmethod
    # Get total number of reviews for a specific product (by name) to calculate total pages on the frontend -- for ProductDetail page
    def count_reviews_for_seller(seller_id):
        rows = app.db.execute('''
        SELECT COUNT(*)
        FROM SellerReview sr
        WHERE sr.seller_id = :seller_id
        ''', seller_id=seller_id)
        return rows[0][0] if rows and rows[0][0] else 0

    
    @staticmethod
    # Get paginated seller reviews authored by a specific user, along with seller full names
    def get_paginated_seller_reviews_by_user(uid, page, items_per_page):
        offset = (page - 1) * items_per_page # calculate offset
        rows = app.db.execute('''
        SELECT sr.buyer_id, sr.seller_id, sr.rating, sr.comment, sr.date_time, u.firstname AS seller_firstname, u.lastname AS seller_lastname
        FROM SellerReview sr 
        JOIN Users u ON sr.seller_id = u.user_id
        WHERE sr.buyer_id = :uid
        ORDER BY sr.date_time DESC
        LIMIT :items_per_page OFFSET :offset
        ''', uid=uid, items_per_page=items_per_page, offset=offset)
        return [SellerReview(*row) for row in rows]
    
    @staticmethod
    # Get total amount of seller reviews by a user to calculate num pages on frontend
    # Can also use this to get a users review stats!
    def count_seller_reviews_by_user(uid):
        rows = app.db.execute('''
        SELECT COUNT(*)
        FROM SellerReview
        WHERE buyer_id = :uid
        ''', uid=uid)
        return rows[0][0] if rows[0][0] else 0
    
    @staticmethod
    # Get PAGINATED and SORTED reviews for a seller by their ID
    def get_paginated_reviews_for_seller(seller_id, page, items_per_page, sort_by):
        offset = (page - 1) * items_per_page  # offset for pagination

        # Separate into 2 cases:
        # 1) the upvote count special case for top 3 most helpful and then by most recent sorting
        # 2) standard sorting options

        if sort_by == "top_helpful_recent":
            # top 3 most helpful reviews is default by proj requirements for upvote
            top_helpful_reviews = app.db.execute('''
                SELECT sr.buyer_id, u.firstname, u.lastname, sr.seller_id, sr.rating, sr.comment, sr.date_time, COUNT(sru.voter_id) AS upvote_count
                FROM SellerReview sr
                JOIN Users u ON sr.buyer_id = u.user_id
                LEFT JOIN SellerReviewUpvote sru 
                ON sr.buyer_id = sru.buyer_id AND sr.seller_id = sru.seller_id
                WHERE sr.seller_id = :seller_id
                GROUP BY sr.buyer_id, u.firstname, u.lastname, sr.seller_id, sr.rating, sr.comment, sr.date_time
                ORDER BY upvote_count DESC
                LIMIT 3
            ''', seller_id=seller_id)

            # use buyer_id, seller_id to filter out the queries we need!
            top_helpful_ids = [(row[0], row[3]) for row in top_helpful_reviews]

            # get rest of reviews by time
            all_recent_reviews = app.db.execute('''
                SELECT sr.buyer_id, u.firstname, u.lastname, sr.seller_id, sr.rating, sr.comment, sr.date_time, COUNT(sru.voter_id) AS upvote_count
                FROM SellerReview sr
                JOIN Users u ON sr.buyer_id = u.user_id
                LEFT JOIN SellerReviewUpvote sru 
                ON sr.buyer_id = sru.buyer_id AND sr.seller_id = sru.seller_id
                WHERE sr.seller_id = :seller_id AND (sr.buyer_id, sr.seller_id) NOT IN :top_helpful_ids
                GROUP BY sr.buyer_id, u.firstname, u.lastname, sr.seller_id, sr.rating, sr.comment, sr.date_time
                ORDER BY sr.date_time DESC
            ''', seller_id=seller_id, top_helpful_ids=tuple(top_helpful_ids))

            # combine results for special sorting case
            combined_reviews = top_helpful_reviews + all_recent_reviews

            # paginate combined list
            paginated_combined_reviews = combined_reviews[offset : offset + items_per_page]

            return [
                {
                    'buyer_id': row[0],
                    'firstname': row[1],
                    'lastname': row[2],
                    'seller_id': row[3],
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
                "helpful": "upvote_count DESC, sr.date_time DESC",
                "rating_high": "sr.rating DESC",
                "rating_low": "sr.rating ASC",
                "date_newest": "sr.date_time DESC",
                "date_oldest": "sr.date_time ASC"
            }.get(sort_by)

            rows = app.db.execute(f'''
                SELECT sr.buyer_id, u.firstname, u.lastname, sr.seller_id, sr.rating, sr.comment, sr.date_time, COUNT(sru.voter_id) AS upvote_count
                FROM SellerReview sr
                JOIN Users u ON sr.buyer_id = u.user_id
                LEFT JOIN SellerReviewUpvote sru 
                ON sr.buyer_id = sru.buyer_id AND sr.seller_id = sru.seller_id
                WHERE sr.seller_id = :seller_id
                GROUP BY sr.buyer_id, u.firstname, u.lastname, sr.seller_id, sr.rating, sr.comment, sr.date_time
                ORDER BY {sort_column}
                LIMIT :items_per_page OFFSET :offset
            ''', seller_id=seller_id, items_per_page=items_per_page, offset=offset)

            return [
                {
                    'buyer_id': row[0],
                    'firstname': row[1],
                    'lastname': row[2],
                    'seller_id': row[3],
                    'rating': row[4],
                    'comment': row[5],
                    'date_time': row[6],
                    'upvote_count': row[7]
                }
                for row in rows
            ]
    
    ## DICT CONVERSION

    
    def to_dict(self):
        return {
            'buyer_id': self.buyer_id,
            'seller_id': self.seller_id,
            'rating': self.rating,
            'comment': self.comment,
            'date_time': self.date_time.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.date_time, datetime) else self.date_time, 
            'seller_firstname': self.seller_firstname,
            'seller_lastname':self.seller_lastname
        }