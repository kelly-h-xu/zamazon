from flask import jsonify, Blueprint, request
from flask_login import current_user
from .models.seller_review import SellerReview
from .models.product_review import ProductReview
from .models.product_review_upvote import ProductReviewUpvote
from .models.seller_review_upvote import SellerReviewUpvote
from .models.buys import Buys
from datetime import datetime

bp = Blueprint('social', __name__)

## PRODUCT REVIEWS APIs ###

# Incorporate fulfillment status check into writing reviews (only write reviews for fulfilled orders - this is on the frontend/by structure of queries)
# Count the amount of fulfilled purchases of a product to determine whether a user can write a review -- ProductDetailPage
@bp.route('/count_fulfilled_purchases_of_product/<product_name>', methods = ['GET'])
def count_fulfilled_purchases_of_product(product_name):
    # by nature of where query is executed, currently don't need to check auth
    if not current_user.is_authenticated:
        return jsonify({"count_purchases": False, "error": "Unauthorized"}), 401
    count_purchases = Buys.count_fulfilled_purchases_of_product(product_name, current_user.id) # use current user id
    return jsonify({"count_purchases": count_purchases}), 200

# Get the review for a specified product by current user -- ProductDetailPage "My Review" Component
@bp.route('/get_product_review/<product_name>', methods = ['GET'])
def get_product_review(product_name):
    # only get review if user logged in
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # query db to grab full product review tuple with current_user id and product_name
    product_review = ProductReview.get_product_review(current_user.id, product_name) # current_user.uid
    if product_review:
        product_review_dict = product_review.to_dict() # convert to dictionary
        return jsonify({'product_review': product_review_dict}), 200
    else:
        return jsonify({'product_review': []}), 200 # empty, no review yet

# Get all of the reviews for a specific product by the name of the product --- for ProductDetail page
# Note currently used, was endpoint used for milestone
@bp.route('/get_all_reviews_for_product/<product_name>', methods = ['GET']) # this API is case sensitive
def get_all_reviews_for_product_by_name(product_name):
    # check input
    if not product_name:
        return jsonify({'error': 'Missing product_name'}), 400
    # query db to grab full product review tuples for products with product_name
    product_reviews = ProductReview.get_all_reviews_for_product_by_name(product_name)
    if product_reviews:
        product_reviews_dict = product_reviews.to_dict() # convert to dictionary
        return jsonify({'product_reviews': product_reviews_dict}), 200
    else:
        return jsonify({'product_reviews': None}), 200 # empty, no reviews yet

# Get the PAGINATED and SORTED overall/average rating for a product -- for ProductDetail page 
@bp.route('/get_paginated_reviews_for_product/<product_name>', methods=['GET'])
def get_paginated_reviews_for_product_by_name(product_name):
    if not product_name:
        return jsonify({'error': 'Missing product_name'}), 400
    
    # Get pagination and sorting parameters from request arguments
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('itemsPerPage', 5))
    sort_by = request.args.get('sortBy', 'helpful')  # Default sort is "Most Helpful"

    # Fetch paginated and sorted reviews and total count from the database
    product_reviews = ProductReview.get_paginated_reviews_for_product_by_name(
        product_name, page, items_per_page, sort_by
    )
    total_reviews = ProductReview.count_reviews_for_product_by_name(product_name)
    total_pages = (total_reviews + items_per_page - 1) // items_per_page
    
    return jsonify({
        'product_reviews': product_reviews,
        'total_pages': total_pages
    }), 200
    
# Get the rating summary for a product -- ProductDetailPage
@bp.route('/get_product_rating_summary/<product_name>', methods = ['GET'])
def get_product_rating_summary(product_name):
    if not product_name:
        return jsonify({'error': 'Missing product_name'}), 400
    product_rating_summary = ProductReview.get_product_rating_summary(product_name)
    return jsonify(product_rating_summary), 200

## PRODUCT REVIEW MODIFICATION ENDPOINTS ##

# Write new product review - this request is only allowed to be made when the order is fulfilled
@bp.route('/new_product_review', methods = ['POST'])
def new_product_review():
    # only a logged in user can write a review
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # request data from frontend
    data = request.json
    product_name = data.get('product_name')
    rating = data.get('rating')
    comment = data.get('comment')
    # query db to insert new product review into ProductReview
    date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S") # add timestamp
    success = ProductReview.new_product_review(product_name, current_user.id, rating, comment, date_time)
    if success:
        return jsonify({"status": "Product review written successfully"}), 200
    else:
        return jsonify({"status": "Failed to write product review"}), 500

# Edit product review
@bp.route('/edit_product_review', methods = ['POST'])
def edit_product_review():
    # only the current user can edit their own review
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # make sure that on the frontend pass in the existing values if the user did not modify a field
    data = request.json
    product_name = data.get('product_name')
    rating = data.get('rating')
    comment = data.get('comment')
    date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S") # add timestamp
    # NOTE - updating a review resets the "time written"
    success = ProductReview.edit_product_review(product_name, current_user.id, rating, comment, date_time)
    if success:
        return jsonify({"status": "Product review edited successfully"}), 200
    else:
        return jsonify({"status": "Failed to edit product review"}), 500

# Delete product review
@bp.route('/delete_product_review/<product_name>', methods = ['DELETE'])
def delete_product_review(product_name):
    # only the current user can delte their own review
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # delete all upvotes associated with the product review before deleting the review
    success1 = ProductReviewUpvote.delete_product_review_upvotes(product_name, current_user.id)
    # delete product review
    success2 = ProductReview.delete_product_review(product_name, buyer_id=current_user.id)
    if success1 and success2:
        return jsonify({"status": "Product review deleted successfully"}), 200
    else:
        return jsonify({"status": "Failed to delete product review"}), 500

## SELLER REVIEWS APIs ##

# Incorporate fulfillment status check into writing reviews (only write reviews for fulfilled orders)
# Count the amount of fulfilled purchases of product by a seller to determine whether a user can write a review -- SellerDetail
@bp.route('/count_fulfilled_purchases_of_seller_products/<seller_id>', methods = ['GET'])
def count_fulfilled_purchases_of_seller_products(seller_id):
    # by nature of where query is executed, currently don't need to check auth
    if not current_user.is_authenticated:
        return jsonify({"count_purchases": False, "error": "Unauthorized"}), 401
    count_purchases = Buys.count_fulfilled_purchases_of_seller_products(seller_id, current_user.id)
    return jsonify({"count_purchases": count_purchases}), 200

# Get the review for a specified seller by current user -- UserDetailPage "My Review" Component
@bp.route('/get_seller_review/<seller_id>', methods = ['GET'])
def get_seller_review(seller_id):
    # only get review if user logged in
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # query db to grab full seller review tuple with current_user id and seller_name
    seller_review = SellerReview.get_seller_review(current_user.id, seller_id)
    if seller_review:
        seller_review_dict = seller_review.to_dict() # convert to dictionary
        return jsonify({'seller_review': seller_review_dict}), 200
    else:
        return jsonify({'seller_review': []}), 200 # empty, no review yet
    
# Get all reviews for a seller by all users
@bp.route('/get_all_reviews_for_seller/<seller_id>', methods = ['GET'])
def get_all_reviews_for_seller(seller_id):
    # check input
    if not seller_id:
        return jsonify({'error': 'Missing seller_id'}), 400
    # query db to grab full review tuples with seller_id
    seller_reviews = SellerReview.get_all_reviews_for_seller(seller_id)
    if seller_reviews:
        seller_reviews_list = [review.to_dict() for review in seller_reviews]
        return jsonify(seller_reviews_list), 200
    else:
        return jsonify({'seller_reviews': []}), 200 # empty, no reviews yet

# Get the overall/average rating for a specific seller
@bp.route('/get_average_rating_for_seller/<seller_id>', methods = ['GET'])
def get_average_rating_for_seller(seller_id):
    # check input
    if not seller_id:
        return jsonify({'error': 'Missing seller_id'}), 400
    # query db to calculate and grab average rating for seller
    average_rating = SellerReview.get_average_rating_for_seller(seller_id)
    if average_rating:
        return jsonify({'average_rating': average_rating}), 200
    else:
        return jsonify({'average_rating': None}), 200 # empty, no ratings exist yet
    
# Get the rating summary for a seller -- UserDetailPage
@bp.route('/get_seller_review_summary/<user_id>', methods = ['GET'])
def get_seller_review_summary(user_id):
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
    seller_review_summary = SellerReview.get_seller_review_summary(user_id)
    return jsonify(seller_review_summary), 200

# Get the PAGINATED and SORTED overall/average rating for a seller -- for UserDetail page 
@bp.route('/get_paginated_reviews_for_seller/<seller_id>', methods=['GET'])
def get_paginated_reviews_for_seller(seller_id):
    # Get pagination and sorting parameters from request arguments
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('itemsPerPage', 5))
    sort_by = request.args.get('sortBy', 'helpful')  # Default sort is "Most Helpful"

    # Fetch paginated and sorted reviews and total count from the database
    seller_reviews = SellerReview.get_paginated_reviews_for_seller(seller_id, page, items_per_page, sort_by)
    total_reviews = SellerReview.count_reviews_for_seller(seller_id)
    total_pages = (total_reviews + items_per_page - 1) // items_per_page
    
    return jsonify({
        'seller_reviews': seller_reviews,
        'total_pages': total_pages
    }), 200

## CREATE/UPDATE/DELETE SellerReview Queries ##

# Write seller review
@bp.route('/new_seller_review', methods = ['POST'])
def new_seller_review():
    # only the current user can write a new review - this query can only be accesses in components after checking fulfillment status
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # switch to request body later, test in URL for now
    data = request.json
    seller_id = data.get('seller_id')
    rating = data.get('rating')
    comment = data.get('comment')
    # query db and insert new seller review
    date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S") # add timestamp
    success = SellerReview.new_seller_review(seller_id, current_user.id, rating, comment, date_time)
    if success:
        return jsonify({"status": "Seller review written successfully"}), 200
    else:
        return jsonify({"status": "Failed to edit seller review"}), 500

# Edit seller review
@bp.route('/edit_seller_review', methods = ['POST'])
def edit_seller_review():
    # only the current user can edit their review
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # make sure that on the frontend pass in the existing values if the user did not modify a field
    data = request.json
    seller_id = data.get('seller_id')
    rating = data.get('rating')
    comment = data.get('comment')
    date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S") # add timestamp
    # NOTE - updating a review resets the "time written"
    success = SellerReview.edit_seller_review(seller_id, current_user.id, rating, comment, date_time)
    if success:
        return jsonify({"status": "Seller review edited successfully"}), 200
    else:
        return jsonify({"status": "Failed to edit seller review"}), 500

# Delete seller review
@bp.route('/delete_seller_review/<int:seller_id>', methods = ['DELETE'])
def delete_seller_review(seller_id):
    # only the current user can delete their review
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    # delete all upvotes associated with the seller review before deleting the review
    success1 = SellerReviewUpvote.delete_seller_review_upvotes(seller_id=seller_id, buyer_id=current_user.id)
    # delete the seller review
    success2 = SellerReview.delete_seller_review(seller_id, current_user.id)
    if success1 and success2:
        return jsonify({"status": "Seller review deleted successfully"}), 200
    else:
        return jsonify({"status": "Failed to delete seller review"}), 500
    
## UPVOTE ENDPOINTS ##
# endpoints that allow for upvote modification, add upvote info in other endpoints to more easily display

## PRODUCT REVIEW UPVOTE ENDPOINTS ##

# Get the total number of upvotes for a specific product review, and the upvotes associated with it
@bp.route('/get_product_review_upvotes/<product_name>/<int:buyer_id>', methods = ['GET'])
def get_product_review_upvotes(product_name, buyer_id):
    product_review_upvotes = ProductReviewUpvote.get_product_review_upvotes(product_name, buyer_id)
    return jsonify({'product_review_upvote_info' : product_review_upvotes}), 200

# Check whether a user has upvotes a product review
@bp.route('/check_user_product_review_upvote/<product_name>/<int:buyer_id>', methods = ['GET'])
def check_user_product_review_upvote(product_name, buyer_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    has_upvote = ProductReviewUpvote.check_user_product_review_upvote(product_name, buyer_id, current_user.id)
    if has_upvote:
        return jsonify({"status": 1 }), 200 # product review upvote does exists (can remove upvote)
    else:
        return jsonify({"status": 0}), 200 # product review upvote does not exist (can upvote)

# Upvote a product review
@bp.route('/upvote_product_review/<product_name>/<int:buyer_id>', methods = ['POST'])
def upvote_product_review(product_name, buyer_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    success = ProductReviewUpvote.upvote_product_review(product_name, buyer_id, current_user.id)
    if success:
        return jsonify({"status": "Product review upvoted successfully"}), 200
    else:
        return jsonify({"status": "Failed to upvote product review"}), 500

# Remove upvote from a product review
@bp.route('/remove_upvote_product_review/<product_name>/<int:buyer_id>', methods = ['POST'])
def remove_upvote_product_review(product_name, buyer_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    success = ProductReviewUpvote.remove_upvote_product_review(product_name, buyer_id, current_user.id)
    if success:
        return jsonify({"status": "Product review upvote deleted successfully"}), 200
    else:
        return jsonify({"status": "Failed to delete product review upvote"}), 500
    
## SELLER REVIEW UPVOTE ENDPOINTS ##

# Get the total number of upvotes for a specific seller review, and the upvotes associated with it
@bp.route('/get_seller_review_upvotes/<int:seller_id>/<int:buyer_id>', methods = ['GET'])
def get_seller_review_upvotes(seller_id, buyer_id):
    seller_review_upvotes = SellerReviewUpvote.get_seller_review_upvotes(seller_id, buyer_id)
    return jsonify({'seller_review_upvote_info' : seller_review_upvotes}), 200

# Check whether a user has upvoted a seller review
@bp.route('/check_user_seller_review_upvote/<int:seller_id>/<int:buyer_id>', methods = ['GET'])
def check_user_seller_review_upvote(seller_id, buyer_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    has_upvote = SellerReviewUpvote.check_user_seller_review_upvote(seller_id, buyer_id, current_user.id)
    if has_upvote:
        return jsonify({"status": 1 }), 200 # seller review upvote does exists (can remove upvote)
    else:
        return jsonify({"status": 0}), 200 # seller review upvote does not exist (can upvote)

# Upvote a seller review
@bp.route('/upvote_seller_review/<int:seller_id>/<int:buyer_id>', methods = ['POST'])
def upvote_seller_review(seller_id, buyer_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    success = SellerReviewUpvote.upvote_seller_review(seller_id, buyer_id, current_user.id)
    if success:
        return jsonify({"status": "Seller review upvoted successfully"}), 200
    else:
        return jsonify({"status": "Failed to upvote seller review"}), 500

# Remove upvote from a seller review
@bp.route('/remove_upvote_seller_review/<int:seller_id>/<int:buyer_id>', methods = ['POST'])
def remove_upvote_seller_review(seller_id, buyer_id):
    if not current_user.is_authenticated:
        return jsonify({"error": "Unauthorized"}), 401
    success = SellerReviewUpvote.remove_upvote_seller_review(seller_id, buyer_id, current_user.id)
    if success:
        return jsonify({"status": "Seller review upvote deleted successfully"}), 200
    else:
        return jsonify({"status": "Failed to delete seller review upvote"}), 500

### APIS USEFUL FOR BOTH PRODUCTS AND SELLERS PAGES ###

# Get all reviews of a specific "sold version" product (all of the unique product ids (determined by diff sellers) for a specific product)
# Get the overall/average rating for a specific product (by the product id, corresponding to a specific seller)
@bp.route('/get_average_rating_for_product_by_id/<product_id>', methods = ['GET'])
def get_average_rating_for_product_by_id(product_id):
    # check input
    if not product_id:
        return jsonify({'error': 'Missing product_id'}), 400
    # query db to calculate and grab average rating for product_id products
    average_rating = ProductReview.get_average_rating_for_product_by_id(product_id)
    if average_rating:
        return jsonify({'average_rating': average_rating}), 200
    else:
        return jsonify({'average_rating': None}), 200 # empty, no ratings exist yet

# Get k most recent product and seller reviews authored by a specific user, along with product names
# NOT IN USE - was used in first milestone but no longer!
# @bp.route('/my_k_most_recent_reviews', methods = ['GET'])
# def k_most_recent_profile_reviews():
#     if current_user.is_authenticated: 
#         recent_product_reviews = ProductReview.get_k_recent_product_reviews_by_user(current_user.uid, 5)
#         recent_seller_reviews = SellerReview.get_k_recent_seller_reviews_by_user(current_user.uid, 5)
        
#         # convert reviews to dictionary (using to_dict method)
#         product_reviews_dict = [review.to_dict() for review in recent_product_reviews]
#         seller_reviews_dict = [review.to_dict() for review in recent_seller_reviews]
        
#         return jsonify({
#             'product_reviews': product_reviews_dict,
#             'seller_reviews': seller_reviews_dict
#         }), 200
#     else:
#         return jsonify({'message': 'Unauthorized'}), 401


# Display user's social center in Public View
# Get all paginated product reviews and all paginated seller reviews
@bp.route('/user_reviews/<int:author_id>', methods = ['GET'])
def get_paginated_reviews_by_author(author_id):
    # grab info about pagination from frontend
    product_page = int(request.args.get('productPage', 1))
    items_per_product_page = int(request.args.get('itemsPerProductPage', 5))
    seller_page = int(request.args.get('sellerPage', 1))
    items_per_seller_page = int(request.args.get('itemsPerSellerPage', 5))
    
    # make request for items in backend
    product_reviews = ProductReview.get_paginated_product_reviews_by_user(author_id, product_page, items_per_product_page)
    seller_reviews = SellerReview.get_paginated_seller_reviews_by_user(author_id, seller_page, items_per_seller_page)
    # make request for total reviews for pagination
    total_product_reviews = ProductReview.count_product_reviews_by_user(author_id)
    total_product_pages = (total_product_reviews + items_per_product_page - 1) // items_per_product_page
    total_seller_reviews = SellerReview.count_seller_reviews_by_user(author_id)
    total_seller_pages = (total_seller_reviews + items_per_seller_page - 1) // items_per_seller_page        
    # convert reviews to dictionary (using to_dict method)
    product_reviews_dict = [review.to_dict() for review in product_reviews]
    seller_reviews_dict = [review.to_dict() for review in seller_reviews]
    
    return jsonify({
        'product_reviews': product_reviews_dict,
        'product_total_pages': total_product_pages,
        'seller_reviews': seller_reviews_dict,
        'seller_total_pages' : total_seller_pages
    }), 200

# # Display user's social center in My Account
# # Get all paginated product reviews and all paginated seller reviews
@bp.route('/my_reviews', methods = ['GET'])
def get_paginated_reviews_by_user():
    if current_user.is_authenticated: 
        # grab info about pagination from frontend
        product_page = int(request.args.get('productPage', 1))
        items_per_product_page = int(request.args.get('itemsPerProductPage', 5))
        seller_page = int(request.args.get('sellerPage', 1))
        items_per_seller_page = int(request.args.get('itemsPerSellerPage', 5))
        
        # make request for items in backend
        product_reviews = ProductReview.get_paginated_product_reviews_by_user(current_user.uid, product_page, items_per_product_page)
        seller_reviews = SellerReview.get_paginated_seller_reviews_by_user(current_user.uid, seller_page, items_per_seller_page)
        # make request for total reviews for pagination
        total_product_reviews = ProductReview.count_product_reviews_by_user(current_user.uid)
        total_product_pages = (total_product_reviews + items_per_product_page - 1) // items_per_product_page
        total_seller_reviews = SellerReview.count_seller_reviews_by_user(current_user.uid)
        total_seller_pages = (total_seller_reviews + items_per_seller_page - 1) // items_per_seller_page        
        # convert reviews to dictionary (using to_dict method)
        product_reviews_dict = [review.to_dict() for review in product_reviews]
        seller_reviews_dict = [review.to_dict() for review in seller_reviews]
        
        return jsonify({
            'product_reviews': product_reviews_dict,
            'product_total_pages': total_product_pages,
            'seller_reviews': seller_reviews_dict,
            'seller_total_pages' : total_seller_pages
        }), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401


@bp.route('/get_seller_reviews_by/<int:user_id>', methods=['GET'])
def get_seller_reviews_by(user_id):
    try:
        # Fetch reviews for the specified user_id
        reviews = SellerReview.get_seller_reviews_by_buyer(user_id)
        
        # If there are no reviews, return a message
        if not reviews:
            return jsonify({"message": "No reviews found for this user."}), 404
        
        # Return the reviews as a list of dictionaries
        review_list = [{
            "buyer_id": review.buyer_id,
            "seller_id": review.seller_id,
            "rating": review.rating,
            "comment": review.comment,
            "date_time": review.date_time
        } for review in reviews]
        
        return jsonify(review_list), 200
        
    except Exception as e:
        return jsonify({"message": "An error occurred while fetching reviews", "error": str(e)}), 500

@bp.route('/get_product_reviews_by/<int:user_id>', methods=['GET'])
def get_product_reviews_by(user_id):
    try:
        # Fetch reviews for the specified user_id
        reviews = ProductReview.get_product_reviews_by_buyer(user_id)
        
        # If there are no reviews, return a message
        if not reviews:
            return jsonify({"message": "No reviews found for this user."}), 404
        
        # Return the reviews as a list of dictionaries
        review_list = [{
            "buyer_id": review.buyer_id,
            "product_name": review.product_name,
            "rating": review.rating,
            "comment": review.comment,
            "date_time": review.date_time
        } for review in reviews]
        
        return jsonify(review_list), 200
        
    except Exception as e:
        return jsonify({"message": "An error occurred while fetching reviews", "error": str(e)}), 500