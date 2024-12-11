// IMPORTS
import React, { useState, useContext, useEffect } from "react";
import axios from "axios";
import { AuthContext } from "../AuthContext"; 
import { baseURL } from "../../config";
import "../styles/Socials/SellerUpvote.css";

// SELLER UPVOTE Component (Seller Review)
function SellerUpvoteComponent({ sellerId, buyerId, upvoteCount, fetchReviews }) {
  const [hasUpvoted, setHasUpvoted] = useState(false); // track upvote status
  const { isAuthenticated } = useContext(AuthContext); // check authentication status

  // Fetch initial upvote status and login status
  useEffect(() => {
    const fetchUpvoteAndLoginStatus = async () => {
      try {
        // If logged in, fetch upvote status
        if (isAuthenticated) {
          const response = await axios.get(
            `${baseURL}/check_user_seller_review_upvote/${sellerId}/${buyerId}`,
            { withCredentials: true }
          );
          setHasUpvoted(response.data.status === 1); // 1 means they have upvoted!
        }
      } catch (error) {
        console.error("Error fetching upvote or login status:", error);
      }
    };

    fetchUpvoteAndLoginStatus();
  }, [sellerId, buyerId]);

  // Handle upvote functionality
  const handleUpvote = async () => {
    try {
      const response = await axios.post(
        `${baseURL}/upvote_seller_review/${sellerId}/${buyerId}`,
        {},
        { withCredentials: true }
      );
      console.log(response.data.status);
      setHasUpvoted(true);
      fetchReviews();
    } catch (error) {
      console.error("Error upvoting review:", error);
      console.log("Failed to upvote review");
    }
  };

  // Handle remove upvote functionality
  const handleRemoveUpvote = async () => {
    try {
      const response = await axios.post(
        `${baseURL}/remove_upvote_seller_review/${sellerId}/${buyerId}`,
        {},
        { withCredentials: true }
      );
      console.log(response.data.status);
      setHasUpvoted(false);
      fetchReviews();
    } catch (error) {
      console.error("Error removing upvote:", error);
      console.log("Failed to remove upvote");
    }
  };

  return (
    <div className="seller-upvote-container">
      <p>Upvotes: {upvoteCount}</p>
      {isAuthenticated && ( // render upvote controls only if the user is logged in
        hasUpvoted ? (
          <p className="remove-upvote" onClick={handleRemoveUpvote}>
            ❌
          </p>
        ) : (
          <p className="upvote-button" onClick={handleUpvote}>
            ⬆️
          </p>
        )
      )}
    </div>
  );
}

export default SellerUpvoteComponent;
