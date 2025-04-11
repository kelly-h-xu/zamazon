from flask import current_app as app

class SellerReviewUpvote:
    def __init__(self, buyer_id, seller_id, voter_id):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.voter_id = voter_id

    @staticmethod
    # Get the total number of upvotes for a specific seller review
    def get(buyer_id, seller_id):
        rows = app.db.execute('''
        SELECT COUNT(*) AS upvote_count
        FROM SellerReviewUpvote sru
        WHERE sru.buyer_id = :buyer_id AND sru.seller_id = :seller_id
        ''', buyer_id=buyer_id, seller_id=seller_id)
                
        return rows[0]['upvote_count'] if rows else 0
    
    @staticmethod
    # Check if a user has an upvote
    def check_user_seller_review_upvote(seller_id, buyer_id, voter_id):
        rows = app.db.execute('''
        SELECT *
        FROM SellerReviewUpvote
        WHERE seller_id = :seller_id AND buyer_id = :buyer_id AND voter_id = :voter_id
        ''', seller_id=seller_id, buyer_id=buyer_id, voter_id=voter_id)
        return len(rows) > 0  # return true if upvote exists
    
    @staticmethod
    # Upvote a seller review
    def upvote_seller_review(seller_id, buyer_id, voter_id):
        try:
            rows = app.db.execute('''
            INSERT INTO SellerReviewUpvote (seller_id, buyer_id, voter_id)
            VALUES (:seller_id, :buyer_id, :voter_id)
            ''', seller_id=seller_id, buyer_id=buyer_id, voter_id=voter_id)
            return True
        except Exception as e:
            print(f"Failed to write item: {e}")
            return False
        
    @staticmethod
    # Remove upvote for a seller review
    def remove_upvote_seller_review(seller_id, buyer_id, voter_id):
        try:
            rows = app.db.execute('''
                DELETE 
                FROM SellerReviewUpvote
                WHERE seller_id = :seller_id AND buyer_id = :buyer_id AND voter_id = :voter_id
                ''', seller_id=seller_id, buyer_id=buyer_id, voter_id=voter_id)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False
    
    @staticmethod
    # Remove all upvotes for a seller review (in the case that a seller review is deleted)
    def delete_seller_review_upvotes(seller_id, buyer_id):
        try:
            rows = app.db.execute('''
                DELETE
                FROM SellerReviewUpvote
                WHERE seller_id = :seller_id AND buyer_id = :buyer_id
                ''', seller_id=seller_id, buyer_id=buyer_id)
            return True
        except Exception as e:
            print(f"Failed to delete item: {e}")
            return False