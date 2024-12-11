from werkzeug.security import generate_password_hash
from genProduct import genRandomProductName, genRandomDescription
import csv
from faker import Faker
import random
import os

# TEST inputs
# num_users = 5
# num_sellers = 2 
# num_unique_products = 5 
# num_multiple_products = 2
# total_products = 7
# num_purchases = 5

# # TEST 2 inputs
# num_users = 20
# num_sellers =  10
# num_unique_products = 24
# num_multiple_products = 12
# total_products = 36
# num_purchases = 45

# TEST 3 inputs
# num_users = 50
# num_sellers = 25
# num_unique_products = 1000 
# num_multiple_products= 500
# total_products = 1500
# num_purchases = 1500

# PRODUCTION inputs
num_users = 100
num_sellers = 50
num_unique_products = 2000
num_repeat_products = 1000
total_products = 3000
num_purchases = 2500

images = os.listdir("frontend/public/pixel_plants")
product_review_templates_good = [
                            ["What an ", "!"],
                            ["Can't wait to watch my ", "!"],
                            ["I'm so happy with my ", "!"],
                            ["I love my ", "!"],
                            ["I'm so excited to munch on my ", "!"]
                            ]
product_review_templates_average = [
                            ["I'm so-so about my ", "."],
                            ["I'm not sure how I feel about my ", "."],
                            ["I'm not sure if I like my ", "."],
                            ["I'm not sure if I want to keep my ", "."],
                            ["I'm not sure if I want to return my ", "."]
                            ]
product_review_templates_bad = [
                            ["I'm so disappointed with my ", "."],
                            ["I wish I could return my ", "."],
                            ["My ", " was a huge disappointment."], 
                            ["I'm so sad about my ", "."],
                            ["I'm so upset about my ", "."]
                            ]   
seller_review_templates_good = [
                            ["I had a great experience with ", "!"],
                            ["I'm so happy with my purchase from ", "!"],
                            ["I love shopping with ", "!"],
                            ["I'm so excited to buy more from ", "!"],
                            ]   
seller_review_templates_average = [
                            ["I'm so-so about my purchase from ", "."],
                            ["I'm not sure how I feel about my purchase from ", "."],
                            ["I'm not sure if I like my purchase from ", "."],
                            ["I'm not sure if I want to keep my purchase from ", "."],
                            ["I'm not sure if I want to return my purchase from ", "."]
                            ]
seller_review_templates_bad = [
                            ["I'm so disappointed with my purchase from ", "."],
                            ["I wish I could return my purchase from ", "."],
                            ["My experience with ", " was a huge disappointment."], 
                            ["I'm so sad about my purchase from ", "."],
                            ["I'm so upset about my purchase from ", "."]
                            ]

Faker.seed(0)
fake = Faker()

def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

"""
Generates users
"""
def gen_users(num_users):
    with open('db/generated/Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        users_map = {}
        for uid in range(num_users):
            if uid % 100 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password) # do we want to pass the hashed password?
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.address()
            balance = 0
            users_map[uid] = [uid, email, address, balance, firstname, lastname, password]
            writer.writerow([uid, email, address, balance, firstname, lastname, password])
        print(f'{num_users} generated')
    return users_map

'''
Gets num_sellers unique user ids from users (to assign them as sellers)
'''
def gen_sellers(num_users, num_sellers):
    seller_id_list = random.sample(range(num_users), num_sellers)
    with open('db/generated/Sellers.csv', 'w') as f:
        writer = get_csv_writer(f)
        for seller_id in seller_id_list:
            writer.writerow([seller_id])
    print(f'Sellers... {num_sellers} generated')
    return seller_id_list

'''
To account for the requirement that multiple sellers can sell the same thing(s).

IMPORTANT!!! We start building products_map here, but finish it in gen_product_listing. 
Call gen_product_catalogs first, then gen_product_listing. Use the products_map that's returned by gen_product_listing.

Details:
- products_map should be an empty dictionary 
- Categories are preset in the genProduct.py file - 4 categories for our plants

- Relies on gen_sellers (more specifically the list of sellers returned by gen_sellers)
Since we have seller_id as a product attribute
'''
def gen_product_catalog(num_unique_products, seller_id_list, products_map):
    with open('db/generated/ProductCatalog.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Product...', end=' ', flush=True)
        product_names = set()
        for pid in range(num_unique_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)

            name, category = genRandomProductName()

            # if name in already generated names, regenerate until get unique one
            while name in product_names:
                name, category = genRandomProductName() 
            product_names.add(name) # else, add the name to the set & proceed

            description = genRandomDescription(name)
            image = random.choice(images)
            image_url = os.path.join("/pixel_plants", image)
            creator_id = random.choice(seller_id_list)

            #the order of products_map that's used by the rest of the functions is:
            # [pid, name, price, category, description, image_url, seller_id, quantity]
            # placeholders for price and quantity for now
            products_map[pid] = [pid, name, 0, category, description, image_url, creator_id, 0]
            writer.writerow([name, category, description, image_url, creator_id])
        print(f'{num_unique_products} generated')
    return products_map #used by gen_product_listings

'''
Details: 
products_map should be the one returned from gen_product_catalog (position 0 of the tuple)

Steps that this function follows: 
1. Assign prices and quantities to the products/sellers from gen_product_catalog 
2. Randomly pick sellers to sell something that's been created by someone else, & fill in info for them
3. we need to finish building products_map to be used by the rest of the functions
'''
def gen_product_listing(seller_id_list, products_map):
    with open('db/generated/ProductListing.csv', 'w') as f:
        writer = get_csv_writer(f)
    
        for product in products_map.values():
            pid = product[0]
            name = product[1]
            seller_id = product[6]
            price = f'{str(fake.random_int(max=200))}.{fake.random_int(max=99):02}'
            quantity = str(fake.random_int(max=1000))

            #update products_map
            products_map[pid][2] = price
            products_map[pid][7] = quantity
            
            writer.writerow([pid, name, seller_id, price, quantity, True])

        #start the ids for the products, after num_unique_products
        for pid in range(num_unique_products, total_products):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)

            #getting the product for this seller to sell, and the info about it    
            p_to_sell = random.choice(list(products_map.keys()))
            name = products_map[p_to_sell][1]
            category = products_map[p_to_sell][3]
            description = products_map[p_to_sell][4]
            image_url = products_map[p_to_sell][5]
            creator_id = products_map[p_to_sell][6]

            #our actual seller id
            seller_id = random.choice(seller_id_list)

            #keep repicking seller_id until we get one that isn't the same as the creator_id
            #(we don't want the same person selling the same products, multiple times in our db
            while seller_id == creator_id:
                seller_id = random.choice(seller_id_list)

            price = f'{str(fake.random_int(max=200))}.{fake.random_int(max=99):02}'
            quantity = str(fake.random_int(max=1000))
            
            #add new entries in products_map
            products_map[pid] = [pid, name, price, category, description, image_url, seller_id, quantity]
            
            writer.writerow([pid, name, seller_id, price, quantity, True])

    return products_map
'''
CartContains(uid, product_id, quantity, at_price)
'''
def gen_cart_contains(products_map):
    with open('db/generated/CartContains.csv', 'w') as f:
        writer = get_csv_writer(f)
        cart_contains_map = {}
        cart_total_price_map = {}
        print('CartContains...', end=' ', flush=True)
        for i in range(len(products_map.values())): 
            if i % 100 == 0:
                print(f'{i}', end=' ', flush=True)

            # need to ensure that we use an existing user id
            uid = random.choice(list(users_map.keys())) 
            
            if uid not in cart_contains_map:
                cart_contains_map[uid] = set()
            
            product_id = random.choice(list(products_map.keys()))
            if product_id not in cart_contains_map[uid]:  # corrected to check within uid set
                cart_contains_map[uid].add(product_id)
                quantity = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
                at_price = float(products_map[product_id][2])
                
                if uid not in cart_total_price_map:
                    cart_total_price_map[uid] = 0
                cart_total_price_map[uid] += at_price * quantity

                # Write entry to CartContains
                writer.writerow([uid, product_id, quantity, at_price])  # only write products that have not already been included in our user's cart

    return cart_contains_map, cart_total_price_map

'''
Cart(uid, total_price)
'''

def gen_cart(cart_total_price_map):

    with open('db/generated/Cart.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        for user in cart_total_price_map:
            uid = user
            total_price = cart_total_price_map[user]
            
            # print(uid, total_price)
            writer.writerow([uid, total_price])
    return

'''
Buys(uid, purchase_id, at_balance)
'''

def gen_buys(orders_list):
    # need to associate each purchase_id with a single user
    # each entry: [purchase_id, cost, date_time, fulfillment_status]
    purchase_id_to_buyer_id_map = {}
    with open('db/generated/Buys.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Buys...', end=' ', flush=True)
        # build map of orders to their corresponding order_contains
        for i in range(len(orders_list)):
            if i % 100 == 0:
                print(f'{i}', end=' ', flush=True) 

            uid = random.choice(list(users_map.keys()))
            purchase_id = orders_contains_list[i][0]
            
            purchase_id_to_buyer_id_map[purchase_id] = uid
            
            at_balance = orders_list[i][1]
                
            writer.writerow([uid, purchase_id, at_balance])
    return purchase_id_to_buyer_id_map

"""
Relies on gen_product_listing to get product_id_list
OrderContains(purchase_id, product_id, at_price, quantity, fulfillment_time)
"""
def gen_order_contains(purchase_id, product_id_list):
    with open('db/generated/OrderContains.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('OrderContains...', end=' ', flush=True)
        orders_contains_map = {} # purchase id : list of order_contains items
        order_contains_list = []
        for oid in range(num_purchases):
            if oid % 100 == 0:
                print(f'{oid}', end=' ', flush=True)
            purchase_id = oid
            product_id = random.choice(product_id_list)
            at_price = fake.random_int(max=500) + 1
            quantity = fake.random_int(max=10) + 1
            fulfillment_status = random.choice([True, False])
            fulfillment_time = 'NULL'
            if fulfillment_status and purchase_id in orders_contains_map:
                fulfillment_time = orders_contains_map[purchase_id][4]
            elif fulfillment_status:
                fulfillment_time = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            data = [purchase_id, product_id, at_price, quantity, fulfillment_time]
            order_contains_list.append(data)
            writer.writerow(data)
        print(f'{num_purchases} generated')
    with open('db/generated/OrderContains.csv', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('\"NULL\"', '')
    with open('db/generated/OrderContains.csv', 'w') as file:
        file.write(filedata)
            
    return order_contains_list

"""
Order(purchase_id, cost, date_time, fulfillment_status)
Generates orders
Relies on gen_order_contains to get order_contains_list
"""
def gen_orders(orders_contains_list):
    with open('db/generated/Orders.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Orders...', end=' ', flush=True)
        orders_map = {}
        # print(orders_contains_list[0]) # DEBUG sanity check that corresponding order_contains is correct
        # build map of orders to their corresponding order_contains
        for i in range(len(orders_contains_list)):
            if i % 100 == 0:
                print(f'{i}', end=' ', flush=True) 
            
            purchase_id = orders_contains_list[i][0]
            cost = orders_contains_list[i][2] * orders_contains_list[i][3]
            date_time = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
            fulfillment_status = False
            if orders_contains_list[i][4] != 'NULL':
                date_time = orders_contains_list[i][4]
                fulfillment_status = True
            
            if purchase_id not in orders_map:
                orders_map[purchase_id] = [purchase_id, cost, date_time, fulfillment_status]
            
            else:
                orders_map[purchase_id][1] += cost
                
            writer.writerow([purchase_id, cost, date_time, fulfillment_status])
            # print([purchase_id, cost, date_time, fulfillment_status]) # DEBUG
        # print(list(orders_map.values())[0]) # DEBUG check that corresponding order_contains is correct 
    return list(orders_map.values())

'''
ProductReview(buyer_id,product_name,rating,comment, date_time)
'''
def gen_product_reviews(good_review_templates, bad_reviews_templates, avg_reviews_templates, orders_list, products_map, purchase_id_to_buyer_id_map, purchase_id_to_product_map):
    fulfilled_orders = [order for order in orders_list if order[3] == True]
    # each entry in orders_list: [purchase_id, cost, date_time, fulfillment_status]
    with open('db/generated/ProductReview.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ProductReview...', end=' ', flush=True)
        existing_reviews = set()
        product_reviews_list = []
        for i in range(len(fulfilled_orders)): # CONFIRM THAT THIS IS TRUE -- CHECK WITH TEAM!
            if i % 100 == 0:
                print(f'{i}', end=' ', flush=True)
            
            purchase_id = fulfilled_orders[i][0]
            
            # need to find the products associated with the purchase_id and loop through them and check each of the products
            products_set = purchase_id_to_product_map[purchase_id]
            
            for product_id in products_set:
                buyer_id = purchase_id_to_buyer_id_map[purchase_id]
                rating = fake.random_int(min=1, max=5)
                if rating > 3:
                    comment = f"{products_map[product_id][1]}".join(random.choice(good_review_templates))
                elif rating == 3:
                    comment = f"{products_map[product_id][1]}".join(random.choice(avg_reviews_templates))
                else:
                    comment = f"{products_map[product_id][1]}".join(random.choice(bad_reviews_templates))
                date_time = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
                
                if (buyer_id, products_map[product_id][1]) not in existing_reviews: # don't allow multiple reviews of the same product by the same buyer
                    existing_reviews.add((buyer_id, products_map[product_id][1]))
                    writer.writerow([buyer_id, products_map[product_id][1], rating, comment, date_time])
                    # print([buyer_id, products_map[product_id][1], rating, comment, date_time]) # DEBUG
                    product_reviews_list.append([buyer_id, products_map[product_id][1], rating, comment, date_time])
    print(f'{len(fulfilled_orders)} generated', flush=True)
    return product_reviews_list
    
# SellerReview(buyer_id,seller_id, rating,comment, date_time) 
def gen_seller_reviews(good_review_templates, bad_reviews_templates, avg_reviews_templates, orders_list, users_map, purchase_id_to_buyer_id_map, purchase_id_to_seller_map):
    fulfilled_orders = [order for order in orders_list if order[3] == True]
    # each entry in orders_list: [purchase_id, cost, date_time, fulfillment_status]
    # print(fulfilled_orders) # DEBUG
    with open('db/generated/SellerReview.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellerReview...', end=' ', flush=True)
        existing_reviews = set()
        seller_reviews_list = []
        for i in range(len(fulfilled_orders)):
            if i % 100 == 0:
                print(f'{i}', end=' ', flush=True)
            
            purchase_id = fulfilled_orders[i][0]
            buyer_id = purchase_id_to_buyer_id_map[purchase_id] # exactly one buyer per purchase
            sellers_set = purchase_id_to_seller_map[purchase_id]
            
            for seller_id in sellers_set:
                # print(users_map[seller_id])
                # will overwrite old reviews of the seller, but this is okay just keep the most recent one
                rating = fake.random_int(min=1, max=5)
                if rating > 3:
                    comment = f"{users_map[seller_id][4]}".join(random.choice(good_review_templates))
                elif rating == 3:
                    comment = f"{users_map[seller_id][4]}".join(random.choice(avg_reviews_templates))
                else:
                    comment = f"{users_map[seller_id][4]}".join(random.choice(bad_reviews_templates))
                
                date_time = fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S')
                if buyer_id != seller_id and (buyer_id, seller_id) not in existing_reviews: # don't allow self-reviews or multiple reviews of the same seller by the same buyer
                    existing_reviews.add((buyer_id, seller_id))
                    writer.writerow([buyer_id, seller_id, rating, comment, date_time])
                    # print([buyer_id, seller_id, rating, comment, date_time]) # DEBUG
                    seller_reviews_list.append([buyer_id, seller_id, rating, comment, date_time])
        print(f'{len(fulfilled_orders)} generated')
        return seller_reviews_list
    
# ProductReviewUpvote - buyer_id, product_id, voter_id - entire entry is key
def gen_product_review_upvote(product_reviews_list, users_map):
    with open('db/generated/ProductReviewUpvote.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('ProductReviewUpvote...', end=' ', flush=True)
        existing_upvotes = set()
        users_set = set(users_map.keys())
        for product_review in product_reviews_list:
            num_upvotes = random.randint(0, 50)
            for _ in range(num_upvotes):
                # generate tuple buyer_id, product_id, voter_id for that product, add to existing upvotes and write if unique
                buyer_id = product_review[0]
                product_name = product_review[1]
                voter_id = random.choice(list(users_set))
                if (buyer_id, product_name, voter_id) not in existing_upvotes: # maintain key constraints
                    existing_upvotes.add((buyer_id, product_name, voter_id))
                    writer.writerow([buyer_id, product_name, voter_id])
    return None

# SellerReviewUpvote - buyer_id, seller_id, voter_id - entire entry is key
def gen_seller_review_upvote(seller_reviews_list, users_map):
    with open('db/generated/SellerReviewUpvote.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('SellerReviewUpvote...', end=' ', flush=True)
        existing_upvotes = set()
        users_set = set(users_map.keys())
        for seller_review in seller_reviews_list:
            num_upvotes = random.randint(0, 50)
            for _ in range(num_upvotes):
                # generate tuple buyer_id, seller_id, voter_id for that seller, add to existing upvotes and write if unique
                buyer_id = seller_review[0]
                seller_id = seller_review[1]
                voter_id = random.choice(list(users_set))
                if (buyer_id, seller_id, voter_id) not in existing_upvotes: # maintain key constraints
                    existing_upvotes.add((buyer_id, seller_id, voter_id))
                    writer.writerow([buyer_id, seller_id, voter_id])
    return None

if __name__ == "__main__":
    
    # GENERATE USERS TABLE #
    users_map = gen_users(num_users) # user : [uid, email, address, balance, firstname, lastname, plain_password]
    #print("users_map: ", users_map)
    
    # GENERATE SELLERS TABLE #
    seller_id_list = gen_sellers(num_users, num_sellers)
    
    # GENERATE PRODUCTCATALOG TABLE #
    products_map_to_build = gen_product_catalog(num_unique_products, seller_id_list, {}) 

    # GENERATE PRODUCTLISTINGS TABLE #
    products_map_final = gen_product_listing(seller_id_list, products_map_to_build)
    print("products_map_final: ", products_map_final) # DEBUG
    # each entry in products_map_final is product_id : [pid, name, price, category, description, image_url, seller_id, quantity]
    
    # GENERATE CARTCONTAINS TABLE #
    cart_contains_map, cart_total_price_map = gen_cart_contains(products_map_final) # user uid : hashet with the product_id s that are in their cart
    # DEBUGGING for gen_cart_contains
    # print("cart_contains_map: ", cart_contains_map) 
    # print("cart_total_price_map: ", cart_total_price_map) 
    
    # GENERATE CART TABLE #
    gen_cart(cart_total_price_map)
        
    # GENERATE ORDER CONTAINS TABLE #
    orders_contains_list = gen_order_contains(num_purchases, list(range(total_products))) 
    # each entry in orders_contains_list: [purchase_id, product_id, at_price, quantity, fulfillment_time]
    
    purchase_id_to_products_map = {} # purchase_id : List[int] of product_id in that purchase
    purchase_id_to_seller_map = {} # purchase_id : List[int] of seller_id that the buyer has purchased from
    for order in orders_contains_list:
        if order[0] not in purchase_id_to_products_map:
            purchase_id_to_products_map[order[0]] = set()
        product_id = order[1]
        purchase_id_to_products_map[order[0]].add(product_id)

        if order[0] not in purchase_id_to_seller_map:
            purchase_id_to_seller_map[order[0]] = set()
        
        seller_id = products_map_final[order[1]][6]
        purchase_id_to_seller_map[order[0]].add(seller_id)
        
        # products_map has product_id to seller_map
        # each entry in product_map is product_id : [pid, name, price, category, description, image_url, seller_id, quantity]

    #print("purchase_id_to_products_map: ", purchase_id_to_products_map)
    #print("purchase_id_to_seller_map: ", purchase_id_to_seller_map)
        
    #print("orders_contains_list: ", orders_contains_list) # DEBUG  
    
    orders_list = gen_orders(orders_contains_list) 
    # each entry in orders_list: [purchase_id, cost, date_time, fulfillment_status]
    #print("orders_list: ", orders_list) # DEBUG 
    
    purchase_id_to_buyer_id_map = gen_buys(orders_list)
    #print("purchase_id_to_buyer_id_map: ", purchase_id_to_buyer_id_map)
    
    # GENERATE REVIEWS TABLES #
    
    product_reviews_list = gen_product_reviews(product_review_templates_good, product_review_templates_bad, product_review_templates_average, orders_list, products_map_final, purchase_id_to_buyer_id_map, purchase_id_to_products_map)
    seller_reviews_list = gen_seller_reviews(seller_review_templates_good, seller_review_templates_bad, seller_review_templates_average, orders_list, users_map, purchase_id_to_buyer_id_map, purchase_id_to_seller_map)
    
    # GENERATE UPVOTES TABLES #
    
    gen_product_review_upvote(product_reviews_list, users_map)
    gen_seller_review_upvote(seller_reviews_list, users_map)
    