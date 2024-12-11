// IMPORTS
import React, { useState, useContext, useEffect, useCallback } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import SellerReviewForm from "./SellerReviewForm";
import { baseURL } from "../../config";
import { AuthContext } from "../AuthContext";

import "../styles/Socials/MySellerReviews.css";

// MY SELLER REVIEW Component (User Details, Order Details)
// Displays the review interface for a seller and allows the user to write, edit, or delete a review
function MySellerReview({ sellerId, sellerName }) {
  const [review, setReview] = useState(null); // set review data
  const [fulfilledPurchaseCount, setFulfilledPurchaseCount] = useState(0); // fulfilled purchases check to determine what review state to trigger
  const [editing, setEditing] = useState(false); // track editing mode
  const { isAuthenticated } = useContext(AuthContext); // check authentication status

  // Fetch fulfilled purchase count and user's review
  const fetchData = useCallback(async () => {
    console.log("Fetching review and purchase data...");
    console.log("sellerData: ", sellerName);
    try {
      // Fetch fulfilled purchase count
      const purchaseResponse = await axios.get(
        `${baseURL}/count_fulfilled_purchases_of_seller_products/${sellerId}`,
        { withCredentials: true }
      );
      // Set the count based on the data
      setFulfilledPurchaseCount(purchaseResponse.data.count_purchases || 0);

      // Fetch user's review
      const reviewResponse = await axios.get(
        `${baseURL}/get_seller_review/${sellerId}`,
        { withCredentials: true }
      );
      

      // If review response empty, set to null
      if (
        Array.isArray(reviewResponse.data.seller_review) &&
        reviewResponse.data.seller_review.length === 0
      ) {
        setReview(null);
      } else {
        // Else, set the seller review
        setReview(reviewResponse.data.seller_review || null); // not null, we fetched a review!
      }
    } catch (error) {
      // Error messaging
      console.error("Error fetching data:", error);
    }
  }, [sellerId]);

  // Fetch most recent data in db
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Handle review form submission
  const handleReviewFormSubmit = async () => {
    try {
      await fetchData(); // after submitting form we want to display new data for review
      setEditing(false); // exit editing mode
    } catch (error) {
      console.error("Error handling form submit:", error);
    }
  };

  // Handle review deletion
  const handleDeleteReview = async () => {
    if (!window.confirm("Are you sure you want to delete this review?")) return;
    try {
      await axios.delete(`${baseURL}/delete_seller_review/${sellerId}`, {
        withCredentials: true,
      });
      setReview(null); // clear review
    } catch (error) {
      console.error("Failed to delete review:", error);
    }
  };

  // If not authenticated, they can't see their review or write one
  if (!isAuthenticated) {
    return (
      <div className="login-prompt">
        <p>
          {" "}
          Please <Link to="/login"> login </Link> to view or write reviews for
          this seller.{" "}
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="my-seller-review-container">
        <h2>
          My Review for <Link to={`/user/${sellerId}`}>{sellerName}</Link>
        </h2>
        {/* Check if the user has any fulfilled purchases */}
        {fulfilledPurchaseCount === 0 ? (
          <div>
            <p className="no-seller-review">
              {" "}
              You have not purchased this seller or your order is not yet
              fulfilled. Please come back to write a review later.{" "}
            </p>
          </div>
        ) : (
          <div className="review-section">
            {/* Check if the user is editing their review */}
            {editing ? (
              <SellerReviewForm
                formType={review ? "update" : "add"}
                review={review || { rating: 0, comment: "" }} // default empty values for add new review case
                sellerId={sellerId}
                onSubmit={handleReviewFormSubmit} // go to function that updates
                onCancel={() => setEditing(false)} // leave editing mode if cancel
              />
            ) : (
              <>
                {/* Display existing review or a message if no review is written yet */}
                {review ? (
                  <div className="review-details">
                    <p className="stars">
                      {"★".repeat(review.rating)}
                      {"☆".repeat(5 - review.rating)}
                    </p>
                    {/* DECIDED TO ONLY DISPLAY UPVOTE COUNT IN LISTS OF REVIEWS <p className="upvote-count">Upvote Count: {review.upvote_count}</p> */}
                    <p className="comment">"{review.comment}"</p>
                  </div>
                ) : (
                  <p className="no-seller-review">No seller review yet.</p>
                )}

                {/* Show actions based on if review exists or does not */}
                <div className="review-actions">
                  <button
                    className="edit-button"
                    onClick={() => setEditing(true)}
                  >
                    {review ? "Edit Review" : "Write Review"}
                  </button>
                  {review && (
                    <button
                      className="delete-button"
                      onClick={handleDeleteReview}
                    >
                      Delete Review
                    </button>
                  )}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default MySellerReview;
