from flask import current_app as app

class ProductReviewUpvote:
    def __init__(self, buyer_id, product_id, voter_id):
        self.buyer_id = buyer_id
        self.product_id = product_id
        self.voter_id = voter_id

    @staticmethod
    # Get the total number of upvotes for a specific product review
    def get_product_review_upvotes(product_name, buyer_id):
        # get the total count of upvotes
        rows = app.db.execute('''
        SELECT COUNT(*) AS upvote_count
        FROM ProductReviewUpvote pru
        WHERE pru.buyer_id = :buyer_id AND pru.product_name = :product_name
        ''', buyer_id=buyer_id, product_name=product_name)
        upvote_count = rows[0][0] if rows else 0
        
        product_review_upvotes = {
            "upvote_count": upvote_count
        }
        return product_review_upvotes
    
    @staticmethod
    # Check if a user has an upvote
    def check_user_product_review_upvote(product_name, buyer_id, voter_id):
        rows = app.db.execute('''
        SELECT *
        FROM ProductReviewUpvote
        WHERE product_name = :product_name AND buyer_id = :buyer_id AND voter_id = :voter_id
        ''', product_name=product_name, buyer_id=buyer_id, voter_id=voter_id)
        return len(rows) > 0  # return true if upvote exists
    
    @staticmethod
    # Upvote a product review
    def upvote_product_review(product_name, buyer_id, voter_id):
        try:
            rows = app.db.execute('''
            INSERT INTO ProductReviewUpvote (product_name, buyer_id, voter_id)
            VALUES (:product_name, :buyer_id, :voter_id)
            ''', product_name=product_name, buyer_id=buyer_id, voter_id=voter_id)
            return True
        except Exception as e:
            print(f"Failed to write item: {e}")
            return False
        
    @staticmethod
    # Remove upvote for a product review
    def remove_upvote_product_review(product_name, buyer_id, voter_id):
        try:
            rows = app.db.execute('''
                DELETE 
                FROM ProductReviewUpvote
                WHERE product_name = :product_name AND buyer_id = :buyer_id AND voter_id = :voter_id
                ''', product_name=product_name, buyer_id=buyer_id, voter_id=voter_id)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False
        
    @staticmethod
    # Remove all upvotes for a product review (in the case that a product review is deleted)
    def delete_product_review_upvotes(product_name, buyer_id):
        try:
            rows = app.db.execute('''
                DELETE 
                FROM ProductReviewUpvote
                WHERE product_name = :product_name AND buyer_id = :buyer_id
                ''', product_name=product_name, buyer_id=buyer_id)
            return True
        except Exception as e:
            print(f"Failed to delete items: {e}")
            return False