// IMPORTS
import React, { useState } from "react";
import axios from "axios";

import { baseURL } from "../../config";

import "../styles/Socials/ReviewForm.css";

// SELLER REVIEW FORM
function SellerReviewForm({ formType, review, sellerId, onSubmit, onCancel }) {
  const [rating, setRating] = useState(review.rating || 0);
  const [comment, setComment] = useState(review.comment || "");

  const handleSubmit = async (event) => {
      event.preventDefault(); // don't submit when clicking any button
  
      // Review data fields
      const reviewData = {
        seller_id: sellerId, 
        rating: rating,
        comment: comment,
      };

      try {
      if (formType === "update") {
          const response = await axios.post(`${baseURL}/edit_seller_review`, reviewData, { withCredentials: true });
          // console.log("Response from server:", response.data);
          console.log("Seller review updated successfully");
          onSubmit();
      } else if (formType === "add") {
          const response = await axios.post(`${baseURL}/new_seller_review`, reviewData, { withCredentials: true });
          // console.log("Response from server:", response.data);
          console.log("New seller review added successfully");
          onSubmit();
      }
      } catch (error) {
          console.error("Error submitting seller review:", error.response || error);
          console.log(error.response?.data?.error || "Failed to submit seller review");
      }
  };

  return (
      <form className="review-form-container" onSubmit={handleSubmit}>
      {/* Review Rating Form Input */}
      <p>
        <span>Rating:</span> <input type="number" min="1" max="5" value={rating} onChange={(e) => setRating(Number(e.target.value))} required /> ⭐️
      </p>
      {/* Review Comment Form Input */}
      <p className="comment"> 
          <span>Comment:</span> <textarea value={comment} onChange={(e) => setComment(e.target.value)} required /> 
      </p>
      {/* Review Form Action Buttons */}
      <div className="review-form-button-container">
          <button className="submit-button" type="submit">Submit</button>
          <button className="cancel-button" type="button" onClick={onCancel}>Cancel</button>
      </div>
      </form>
    );
  }

export default SellerReviewForm;
  