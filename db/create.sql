CREATE TABLE Users (
    user_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR(127) NOT NULL,
    address VARCHAR(1023) NOT NULL, 
    balance FLOAT, 
    firstname VARCHAR(127) NOT NULL, 
    lastname VARCHAR(127) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Sellers (
    seller_id INT PRIMARY KEY REFERENCES Users(user_id)
);

CREATE TABLE Category (
    category_name VARCHAR(255) NOT NULL PRIMARY KEY
);

CREATE TABLE ProductCatalog(
    product_name VARCHAR(255) NOT NULL PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    description VARCHAR(1023) NOT NULL,
    creator_id INT, 
    FOREIGN KEY (category) REFERENCES Category(category_name),
    FOREIGN KEY (creator_id) REFERENCES Sellers(seller_id)
);

CREATE TABLE ProductListing (
    product_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    product_name VARCHAR(255) NOT NULL,
    seller_id INT NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    quantity INT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT true,
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id),
    FOREIGN KEY (product_name) REFERENCES ProductCatalog(product_name)
);

CREATE TABLE SellerReview (
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(1023),
    date_time TIMESTAMP NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY (buyer_id, seller_id),
    FOREIGN KEY (buyer_id) REFERENCES Users(user_id),
    FOREIGN KEY (seller_id) REFERENCES Sellers(seller_id)
);

CREATE TABLE SellerReviewUpvote (
    buyer_id INT NOT NULL,
    seller_id INT NOT NULL,
    voter_id INT NOT NULL,
    PRIMARY KEY (buyer_id, seller_id, voter_id),
    FOREIGN KEY (buyer_id, seller_id) REFERENCES SellerReview(buyer_id, seller_id),
    FOREIGN KEY (voter_id) REFERENCES Users(user_id)
);

CREATE TABLE ProductReview (
    buyer_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    rating INT NOT NULL,
    comment VARCHAR(1023),
    date_time TIMESTAMP NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    PRIMARY KEY (buyer_id, product_name),
    FOREIGN KEY (buyer_id) REFERENCES Users(user_id),
    FOREIGN KEY (product_name) REFERENCES ProductCatalog(product_name)
);

CREATE TABLE ProductReviewUpvote (
    buyer_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    voter_id INT NOT NULL,
    PRIMARY KEY (buyer_id, product_name, voter_id),
    FOREIGN KEY (buyer_id) REFERENCES Users(user_id),
    FOREIGN KEY (buyer_id, product_name) REFERENCES ProductReview(buyer_id, product_name)
);

-- single order
CREATE TABLE Orders (
    purchase_id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    cost DECIMAL(12,2) NOT NULL,
    date_time TIMESTAMP NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    fulfillment_status BOOLEAN DEFAULT false 
);

-- single item in an order. Use for more itemized details of an order
CREATE TABLE OrderContains (
    purchase_id INT NOT NULL REFERENCES Orders(purchase_id),
    product_id INT NOT NULL REFERENCES ProductListing(product_id),
    quantity INT NOT NULL,
    at_price DECIMAL(12,2) NOT NULL,
    fulfillment_time TIMESTAMP NULL DEFAULT NULL,
    PRIMARY KEY (purchase_id, product_id)
);

CREATE TABLE Cart (
    uid INT NOT NULL PRIMARY KEY,
    total_price DECIMAL(12,2),
    FOREIGN KEY (uid) REFERENCES Users(user_id)
);

CREATE TABLE CartContains (
    uid INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    at_price DECIMAL(12,2),
    PRIMARY KEY (uid, product_id),
    FOREIGN KEY (uid) REFERENCES Users(user_id),
    FOREIGN KEY (product_id) REFERENCES ProductListing(product_id)
);

CREATE TABLE Buys (
    buyer_id INT NOT NULL REFERENCES Users(user_id),
    purchase_id INT NOT NULL REFERENCES Orders(purchase_id), 
    at_balance FLOAT NOT NULL,
    PRIMARY KEY(buyer_id, purchase_id)
);