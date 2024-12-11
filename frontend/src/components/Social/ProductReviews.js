// IMPORTS
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import { Pagination } from "@mui/material";
import ProductUpvoteComponent from "./ProductUpvoteComponent";
import { baseURL } from "../../config";

import "../styles/Products/ProductCard.css";
import "../styles/Socials/Reviews.css";

// PRODUCT REVIEWS Components
// Display and paginate on SQL backend all reviews for product of that name
// By default the top 3 most helpful reviews would be shown first, and then the most recent following these
// Allow sorting by rating (low to high, high to low), by date (low to high, high to low)
// For each rating card display: Seller ID, Author, Stars
// Comment, Number of upvotes, Upvote or remove upvote functionality
function ProductReviews({ productName }) {
  const [reviews, setReviews] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sortBy, setSortBy] = useState("top_helpful_recent"); // DEFAULT SORT BY PROJ REQUIREMENTS
  const itemsPerPage = 2; // product reviews per components page

  // Fetch reviews from the backend, update pagination info
  const fetchReviews = useCallback(async () => {
    try {
      const response = await axios.get(
        `${baseURL}/get_paginated_reviews_for_product/${productName}`,
        {
          params: {
            productName,
            page: currentPage,
            itemsPerPage,
            sortBy,
          },
        }
      );
      setReviews(response.data.product_reviews);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  }, [productName, currentPage, itemsPerPage, sortBy]);

  // Fetch reviews on component mount and when dependencies change
  useEffect(() => {
    fetchReviews();
  }, [fetchReviews]);

  return (
    <div className="product-reviews-container">
      {/* Sorting Options Container */}
      <div className="sort-options">
        <label>Sort By: </label>
        <select
          id="sort"
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
        >
          <option value="helpful">Most Helpful</option>
          <option value="rating_high">Rating: High to Low</option>
          <option value="rating_low">Rating: Low to High</option>
          <option value="date_newest">Date: Newest First</option>
          <option value="date_oldest">Date: Oldest First</option>
          <option value="top_helpful_recent">
            Top 3 Most Helpful, Then Recent
          </option>
        </select>
      </div>

      {/* Display the review items */}
      {reviews.length === 0 ? (
        <p>No reviews found for this product.</p>
      ) : (
        <div>
          <ul className="reviews-list">
            {reviews.map((review) => (
              <li
                key={`${review.product_name}-${review.buyer_id}`}
                className="detail-review-item"
              >
                <div className="product-card">
                  <p>
                    <strong>Author:</strong>{" "}
                    <Link to={`/user/${review.buyer_id}`}>
                      {" "}
                      {review.firstname} {review.lastname}
                    </Link>
                  </p>
                  <p>
                    <strong>Rating:</strong>{" "}
                    {"★".repeat(review.rating) + "☆".repeat(5 - review.rating)}
                  </p>
                  <p>
                    <strong>Comment:</strong> {review.comment}
                  </p>
                  <p>
                    <strong>Posted on:</strong> {review.date_time}
                  </p>
                  <ProductUpvoteComponent productName={review.product_name}
                  buyerId={review.buyer_id}
                  upvoteCount={review.upvote_count}
                  fetchReviews={fetchReviews}></ProductUpvoteComponent>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Pagination Function */}
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

export default ProductReviews;
