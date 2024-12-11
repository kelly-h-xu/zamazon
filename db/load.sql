-- // NEW LOAD.SQL //
\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_user_id_seq',
                         (SELECT MAX(user_id)+1 FROM Users),
                         false);

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Category FROM 'Category.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ProductCatalog FROM 'ProductCatalog.csv' WITH DELIMITER ',' NULL '' CSV
\COPY ProductListing FROM 'ProductListing.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.productlisting_product_id_seq',
                         (SELECT MAX(product_id)+1 FROM ProductListing),
                         false);

\COPY SellerReview FROM 'SellerReview.csv' WITH DELIMITER ',' NULL '' CSV

\COPY SellerReviewUpvote FROM 'SellerReviewUpvote.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ProductReview FROM 'ProductReview.csv' WITH DELIMITER ',' NULL '' CSV

\COPY ProductReviewUpvote FROM 'ProductReviewUpvote.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.orders_purchase_id_seq',
                         (SELECT MAX(purchase_id)+1 FROM Orders),
                         false);

\COPY OrderContains FROM 'OrderContains.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Cart FROM 'Cart.csv' WITH DELIMITER ',' NULL '' CSV

\COPY CartContains FROM 'CartContains.csv' WITH DELIMITER ',' NULL ' ' CSV

\COPY Buys FROM 'Buys.csv' WITH DELIMITER ',' NULL '' CSV
