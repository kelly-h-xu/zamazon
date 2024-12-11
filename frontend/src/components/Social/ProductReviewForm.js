// IMPORTS
import React, { useState } from "react";
import axios from "axios";

import { baseURL } from "../../config";

import "../styles/Socials/ReviewForm.css";

// PRODUCT REVIEW FORM
function ProductReviewForm({ formType, review, productName, onSubmit, onCancel }) {
  const [rating, setRating] = useState(review.rating || 0);
  const [comment, setComment] = useState(review.comment || "");

  const handleSubmit = async (event) => {
    event.preventDefault(); // don't submit when clicking any button
    
    // Review data fields
    const reviewData = {
      product_name: productName,
      rating: rating,
      comment: comment,
    };

    // Debugging logs
    // console.log("Submitting review data:", reviewData);

    try {
      if (formType === "update") {
        const response = await axios.post(`${baseURL}/edit_product_review`, reviewData, { withCredentials: true });
        // console.log("Response from server:", response.data);
        console.log("Review updated successfully");
        onSubmit(); // callback parent
      } else if (formType === "add") {
        const response = await axios.post(`${baseURL}/new_product_review`, reviewData, { withCredentials: true });
        // console.log("Response from server:", response.data);
        console.log("New product review added successfully");
        onSubmit(); // callback parent
      }
    } catch (error) {
      console.error("Error submitting review:", error.response || error);
      console.log(error.response?.data?.error || "Failed to submit review");
    }
  };

  return (
    <form className="review-form-container" onSubmit={handleSubmit}>
        {/* Review Rating Form Input */}
        <label>
          Rating: <input type="number" min="1" max="5" value={rating} onChange={(e) => setRating(Number(e.target.value))} required />
        </label>
        {/* Review Comment Form Input */}
        <label> 
            Comment: <textarea value={comment} onChange={(e) => setComment(e.target.value)} required /> 
        </label>
        {/* Review Form Action Buttons */}
        <div className="review-form-button-container">
            <button className="submit-button" type="submit">Submit</button>
            <button className="cancel-button" type="button" onClick={onCancel}>Cancel</button>
        </div>
      </form>
    );
  }

export default ProductReviewForm;
