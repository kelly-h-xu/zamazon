// IMPORTS
import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import { Pagination } from "@mui/material";
import SellerUpvoteComponent from "./SellerUpvoteComponent";
import { baseURL } from "../../config";

import "../styles/Socials/SellerReviews.css";

// SELLER REVIEWS Component (User Details)
function SellerReviews({ user_id }) {
  // COMPONENT - "Reviews" (by seller)
  // Display and paginate on SQL backend all reviews for seller
  // By default the top 3 most helpful reviews would be shown first, and then the most recent following these
  // Allow sorting by rating (low to high, high to low), by date (low to high, high to low)
  // For each rating card display: Author, Stars, Comment, 
  // Number of upvotes, Upvote or remove upvote functionality

  const [reviews, setReviews] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 3; // Reviews per page
  const [sortBy, setSortBy] = useState("top_helpful_recent");

  // Fetch reviews from backend
  const fetchReviews = async () => {
    try {
      const response = await axios.get(
        `${baseURL}/get_paginated_reviews_for_seller/${user_id}`,
        {
          params: {
            user_id,
            page: currentPage,
            itemsPerPage,
            sortBy,
          },
        }
      );
      setReviews(response.data.seller_reviews);
      setTotalPages(response.data.total_pages);
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  const handleSortChange = (e) => {
    setSortBy(e.target.value);
    setCurrentPage(1); // reset to the first page on sort change
  };

  useEffect(() => {
    fetchReviews();
  }, [currentPage, sortBy]);

  return (
    <div className="seller-reviews-container">
      <h2>Reviews for this Seller</h2>

      <div className="sort-options">
        <label htmlFor="sort">Sort By:</label>
        <select id="sort" value={sortBy} onChange={handleSortChange}>
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

      <ul className="reviews-list">
        {reviews.length > 0 ? (
          reviews.map((review, index) => (
            <li key={index} className="review-item">
              <div className="review-details">
                <p>
                  Review by:{" "}
                  <Link to={`/user/${review.buyer_id}`}>
                    {review.firstname} {review.lastname}
                  </Link>
                </p>
                <p>
                  {"★".repeat(review.rating) + "☆".repeat(5 - review.rating)}
                </p>
                <p>"{review.comment}"</p>
                <p className="date-time">
                  Posted on {new Date(review.date_time).toLocaleString()}
                </p>
              </div>
              <SellerUpvoteComponent
                sellerId={review.seller_id}
                buyerId={review.buyer_id}
                upvoteCount={review.upvote_count}
                fetchReviews={fetchReviews} // refresh after upvote
              />
            </li>
          ))
        ) : (
          <p>No reviews available for this seller.</p>
        )}
      </ul>

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

export default SellerReviews;
