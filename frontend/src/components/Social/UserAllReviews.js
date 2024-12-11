// IMPORTS
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import { Pagination } from "@mui/material"; // Import the Pagination component
import { baseURL } from "../../config";

import "../styles/Socials/UserAllReviews.css";

// USER ALL REVIEWS
function UserAllReviews({ user_id }) {
  const [sellerReviews, setSellerReviews] = useState([]);
  const [productReviews, setProductReviews] = useState([]);
  const [productPage, setProductPage] = useState(1);
  const [sellerPage, setSellerPage] = useState(1);
  const [productTotalPages, setProductTotalPages] = useState(1);
  const [sellerTotalPages, setSellerTotalPages] = useState(1);
  const [error, setError] = useState(null);

  const fetchReviews = async (productPage = 1, sellerPage = 1) => {
    try {
      const response = await axios.get(`${baseURL}/user_reviews/${user_id}`, {
        params: {
          productPage,
          sellerPage,
          itemsPerProductPage: 5, // Adjust if needed
          itemsPerSellerPage: 5,
        },
        withCredentials: true,
      });

      setSellerReviews(response.data.seller_reviews);
      setProductReviews(response.data.product_reviews);
      setProductTotalPages(response.data.product_total_pages);
      setSellerTotalPages(response.data.seller_total_pages);
    } catch (err) {
      setError(
        err.response?.data?.message ||
          "An error occurred while fetching reviews"
      );
    }
  };

  useEffect(() => {
    fetchReviews(productPage, sellerPage);
  }, [productPage, sellerPage]);

  if (error) return <p>Error: {error}</p>;

  return (
    <div className="user-all-revs-container">
      {/* Seller Reviews Section */}
      <div className="reviews-section">
        <h2>Seller Reviews</h2>
        {sellerReviews.length > 0 ? (
          <>
            <ul>
              {sellerReviews.map((review) => (
                <li key={review.seller_id}>
                  <p>
                    Review of{" "}
                    <Link to={`/user/${review.seller_id}`}>
                      {review.seller_firstname} {review.seller_lastname}
                    </Link>
                  </p>
                  <p>
                    {"★".repeat(review.rating) + "☆".repeat(5 - review.rating)}
                  </p>
                  <p>"{review.comment}"</p>
                  <p className="date-time">
                    Posted on {new Date(review.date_time).toLocaleString()}
                  </p>
                </li>
              ))}
            </ul>
            <div className="pagination">
              <Pagination
                count={sellerTotalPages}
                page={sellerPage}
                onChange={(event, page) => setSellerPage(page)}
                shape="rounded"
              />
            </div>
          </>
        ) : (
          <p>No seller reviews available.</p>
        )}
      </div>

      {/* Product Reviews Section */}
      <div className="reviews-section">
        <h2>Product Reviews</h2>
        {productReviews.length > 0 ? (
          <>
            <ul>
              {productReviews.map((review) => (
                <li key={review.product_name}>
                  <p>
                    Review of{" "}
                    <Link
                    to={`/product/${encodeURIComponent(review.product_name)}`}
                    state={{ product_name: review.product_name }}
                  >
                      {review.product_name}
                    </Link>
                  </p>
                  <p>
                    {"★".repeat(review.rating) + "☆".repeat(5 - review.rating)}
                  </p>
                  <p>"{review.comment}"</p>
                  <p className="date-time">
                    Posted on {new Date(review.date_time).toLocaleString()}
                  </p>
                </li>
              ))}
            </ul>
            <div className="pagination">
              <Pagination
                count={productTotalPages}
                page={productPage}
                onChange={(event, page) => setProductPage(page)}
                shape="rounded"
              />
            </div>
          </>
        ) : (
          <p>No product reviews available.</p>
        )}
      </div>
    </div>
  );
}

export default UserAllReviews;
