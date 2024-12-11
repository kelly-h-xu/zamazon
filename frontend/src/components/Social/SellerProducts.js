// IMPORTS
import React, { useEffect, useState } from "react";
import axios from "axios";

import { Pagination } from "@mui/material";
import { baseURL } from "../../config";

import "../styles/Socials/SellerProducts.css";
import "../styles/UserDetailsPage.css";

// SELLER PRODUCTS Component (User Details)
function SellerProducts({ seller_id }) {
  const [products, setProducts] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const itemsPerPage = 2;
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Fetch products from backend when component is 
  // mounted or when seller_id/currentPage changes
  useEffect(() => {
    const fetchProducts = async () => {
      // Validate seller_id entry
      if (!/^\d+$/.test(seller_id) || parseInt(seller_id, 10) < 0) {
        setErrorMessage(
          "ERROR: Seller ID must be an integer greater than or equal to 0."
        );
        // Seller_id is invalid
        return;
      }

      try {
        const response = await axios.get(
          `${baseURL}/get_paginated_products_by_seller/${seller_id}`,
          {
            params: {
              page: currentPage,
              page_size: itemsPerPage,
            },
          }
        );

        const { products, total_count } = response.data;

        // Set products and calculate total pages from the response
        if (products.length > 0) {
          setProducts(products);
          setTotalPages(Math.ceil(total_count / itemsPerPage)); // Use total_count for total pages
        }
      } catch (error) {
        // Error messaging
        console.log("Error loading products by the seller: ", error);
      }
    };

    fetchProducts();
  }, [seller_id, currentPage]);

  return (
    <div className="seller-products-container">
      <h2>Products Sold</h2>

      {/* Products List */}
      {products.length > 0 ? (
        <div className="products-list">
          {products.map((product) => (
            // Map through products array and render each product 
            <div key={product.product_id} className="product-card">
              <div className="product-details">
                <div className="overview">
                  <div className="product-image">
                    {product.image_url ? (
                      <img src={product.image_url} alt={product.description} />
                    ) : (
                      <p>No image available</p>
                    )}
                  </div>
                  <div>
                    <p>
                      {/* <Link to={`/product/${product.product_name}`}> */}
                      {product.product_name}
                      {/* </Link> */}
                    </p>
                    <p>
                      <strong>Product ID:</strong> {product.product_id}
                    </p>
                    <p>
                      <strong>Price:</strong> $
                      {parseFloat(product.price).toFixed(2)}
                    </p>
                    <p>
                      <strong>Quantity:</strong> {product.quantity}
                    </p>
                    <p>
                      <strong>Category:</strong> {product.category}
                    </p>
                  </div>
                </div>
                <p>
                  <strong>Description:</strong> {product.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        // No products found message
        !errorMessage && <p>No products found for Seller {seller_id}.</p>
      )}

      {/* Pagination controls */}
      <div className="pagination">
        <Pagination
          count={totalPages}
          page={currentPage}
          onChange={(event, page) => setCurrentPage(page)}
          shape="rounded"
        />
      </div>
    </div>
  );
}

export default SellerProducts;
