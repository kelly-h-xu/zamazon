// IMPORTS
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";

import MySellerReview from "./Social/MySellerReview";
import SellerProducts from "./Social/SellerProducts";
import SellerRatingSummary from "./Social/SellerRatingSummary";
import SellerReviews from "./Social/SellerReviews";
import UserAllReviews from "./Social/UserAllReviews";
import { baseURL } from "../config";

import "./styles/UserDetailsPage.css";

// USER DETAILS PAGE
const UserDetailsPage = () => {
  const { userId } = useParams(); // Gets the userId from the route params
  const [user, setUser] = useState(null);
  const [isSeller, setIsSeller] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch user details by User ID in 8080 backend
    const fetchUserDetails = async () => {
      try {
        const response = await axios.get(`${baseURL}/user/${userId}`);
        setUser(response.data);
      } catch (err) {
        // Error messaging
        setError(
          err.response?.data?.message ||
            "An error occurred fetching user details"
        );
      }
    };

    // Check if the user is a seller
    const fetchSellerStatus = async () => {
      try {
        const response = await axios.get(`${baseURL}/is_seller/${userId}`);
        setIsSeller(response.data.seller_status); // Set the seller status
      } catch (err) {
        setError(
          err.response?.data?.message ||
            "An error occurred fetching seller status"
        );
      }
    };

    fetchUserDetails();
    fetchSellerStatus();
  }, [userId]);

  // Error messaging
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      {user ? (
        <div className="user-details-container">
          <h1>
            <strong>User #{user.user_id}:</strong> {user.firstname}{" "}
            {user.lastname}
          </h1>

          {/* Only display seller-specific components if they are a seller */}
          {isSeller && (
            <>
              <div className="seller-specific">
                {/* Logged user's review for the seller */}
                <MySellerReview sellerId={user.user_id} sellerData={user.firstname} />
                {/* Summary data for the seller */}
                <SellerRatingSummary user_id={user.user_id} />
              </div>
              <div className="seller-specific">
                {/* Review for this seller */}
                <SellerReviews user_id={user.user_id} />
                {/* Products sold by the seller */}
                <SellerProducts seller_id={user.user_id} />
              </div>
            </>
          )}

          {/* General user reviews for products and sellers */}
          <div className="user-reviews">
            <h2>{user.firstname}'s Reviews</h2>
            <UserAllReviews user_id={user.user_id} />
          </div>
        </div>
      ) : (
        // No details messaging
        <p>No user details available</p>
      )}
    </div>
  );
};

export default UserDetailsPage;
