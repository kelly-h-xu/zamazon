// IMPORTS
import React, { useState, useContext, useEffect } from "react";
import axios from "axios";

import { baseURL } from "../../config";
import { AuthContext } from "../AuthContext";

import "../styles/Socials/ProductUpvote.css";

function ProductUpvoteComponent({
  productName,
  buyerId,
  upvoteCount,
  fetchReviews,
}) {
  const [hasUpvoted, setHasUpvoted] = useState(false); // track upvote status
  const { isAuthenticated } = useContext(AuthContext); // check authentication status

  // Fetch initial upvote status and check login status
  useEffect(() => {
    const checkUpvoteStatus = async () => {
      try {
        // If logged in, check upvote status
        if (isAuthenticated) {
          const response = await axios.get(
            `${baseURL}/check_user_product_review_upvote/${productName}/${buyerId}`,
            { withCredentials: true }
          );
          setHasUpvoted(response.data.status === 1); // 1 means they have upvoted!
        }
      } catch (error) {
        console.error("Error checking upvote status:", error);
      }
    };

    checkUpvoteStatus();
  }, [productName, buyerId]);

  // Handle upvote functionality
  const handleUpvote = async () => {
    try {
      const response = await axios.post(
        `${baseURL}/upvote_product_review/${productName}/${buyerId}`,
        {},
        { withCredentials: true }
      );
      alert(response.data.status);
      setHasUpvoted(true);
      fetchReviews();
    } catch (error) {
      console.error("Error upvoting review:", error);
      alert("Failed to upvote review");
    }
  };

  // Handle remove upvote functionality
  const handleRemoveUpvote = async () => {
    try {
      const response = await axios.post(
        `${baseURL}/remove_upvote_product_review/${productName}/${buyerId}`,
        {},
        { withCredentials: true }
      );
      alert(response.data.status);
      setHasUpvoted(false);
      fetchReviews();
    } catch (error) {
      console.error("Error removing upvote:", error);
      alert("Failed to remove upvote");
    }
  };

  return (
    <div className="product-upvote-container">
      <p>
        <strong>Upvotes:</strong> {upvoteCount}
      </p>
      {isAuthenticated && // render upvote controls only if the user is logged in
        (hasUpvoted ? (
          <p className="remove-upvote" onClick={handleRemoveUpvote}>
            ❌
          </p>
        ) : (
          <p className="upvote-button" onClick={handleUpvote}>
            ⬆️
          </p>
        ))}
    </div>
  );
}

export default ProductUpvoteComponent;
