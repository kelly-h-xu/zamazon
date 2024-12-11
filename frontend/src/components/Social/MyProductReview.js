// IMPORTS
import React, { useState, useContext, useEffect, useCallback } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import ProductReviewForm from "./ProductReviewForm.js";
import { baseURL } from "../../config";
import { AuthContext } from "../AuthContext";
import "../styles/Socials/MyProductReview.css";
import "../styles/Products/ProductCard.css";

// MY PRODUCT REVIEW Component (Order Details)
// Display actions for the product (by name)
// ONLY DISPLAY if current user logged in, else display, LOGIN to write a review
// If the user has not purchased this product then display "You have not purchased this product or your order is not yet fulfilled, please come back to write a review later."
// If current user have purchased this product, write/update/delete review
// If review exists, display the review / review form with the above actions
function MyProductReview({ productName }) {
  const [review, setReview] = useState(null); // set review data
  const [fulfilledPurchaseCount, setFulfilledPurchaseCount] = useState(0); // fulfilled purchases check to determine what review state to trigger
  const [editing, setEditing] = useState(false); // track editing mode
  const { isAuthenticated } = useContext(AuthContext); // check authentication status

  // Fetch fulfilled purchase count and user's review
  const fetchData = useCallback(async () => {
    // console.log("Fetching review and purchase data...");
    try {
      // Fetch fulfilled purchase count
      const purchaseResponse = await axios.get(
        `${baseURL}/count_fulfilled_purchases_of_product/${productName}`,
        { withCredentials: true }
      );
      // console.log("Fulfilled Purchase Response:", purchaseResponse.data);
      setFulfilledPurchaseCount(purchaseResponse.data.count_purchases || 0);

      // Fetch user's review
      const reviewResponse = await axios.get(
        `${baseURL}/get_product_review/${productName}`,
        { withCredentials: true }
      );
      // console.log("Review Response:", reviewResponse.data);

      // Check if review response is empty array, if so then set to null!
      if (
        Array.isArray(reviewResponse.data.product_review) &&
        reviewResponse.data.product_review.length === 0
      ) {
        setReview(null); // set to null
      } else {
        setReview(reviewResponse.data.product_review || null); // not null, we fetched a review!
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }, [productName]);

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
      await axios.delete(`${baseURL}/delete_product_review/${productName}`, {
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
          this product.{" "}
        </p>
      </div>
    );
  }

  return (
    <div className = "product-card">
      <div className="my-product-review-container">
        <h2>My Review for This Product </h2>
        {/* Check if the user has any fulfilled purchases */}
        {fulfilledPurchaseCount === 0 ? (
          <div>
            <p className="no-product-review">
              {" "}
              You have not purchased this product or your order is not yet
              fulfilled. Please come back to write a review later.{" "}
            </p>
          </div>
        ) : (
          <div className="review-section">
            {editing ? (
              <ProductReviewForm
                formType={review ? "update" : "add"}
                review={review || { rating: 0, comment: "" }} // default empty values for add new review case
                productName={productName}
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
                    <p className="comment">{review.comment}</p>
                  </div>
                ) : (
                  <p>No product review yet.</p>
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

export default MyProductReview;
