// IMPORTS
import React, { useState, useEffect } from "react";
import axios from "axios";

import { baseURL } from "../../config";

import "../styles/Socials/SellerRatingSummary.css";

// SELLER RATING SUMMARY Component (User Details)
function SellerRatingSummary({ user_id }) {
  const [ratingSummary, setRatingSummary] = useState({});

  useEffect(() => {
    // Function grabs product rating summary from backend
    const fetchRatingSummary = async () => {
      try {
        const response = await axios.get(
          `${baseURL}/get_seller_review_summary/${user_id}`
        );
        setRatingSummary(response.data);
      } catch (error) {
        console.error("Failed to fetch rating summary:", error);
      }
    };

    // Call function to update review summary
    fetchRatingSummary();
  }, [user_id]);

  return (
    <div className="seller-rating-summary">
      <h2>Seller Rating Summary</h2>
      <div className="seller-rating-summary-details">
        <p>
          🌟 Average Rating:{" "}
          <span>
            {parseFloat(ratingSummary.average_rating).toFixed(2) || "N/A"}
          </span>
        </p>
        <p>
          🔻 Lowest Rating: <span>{ratingSummary.lowest_rating || "N/A"}</span>
        </p>
        <p>
          🔺 Highest Rating:{" "}
          <span>{ratingSummary.highest_rating || "N/A"}</span>
        </p>
        <p>
          🧮 Total Ratings: <span>{ratingSummary.total_ratings || "N/A"}</span>
        </p>
      </div>
    </div>
  );
}

export default SellerRatingSummary;
