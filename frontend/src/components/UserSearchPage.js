// IMPORTS
import React, { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import animalGuy from "../assets/animal_guy.png";
import { baseURL } from "../config";

import "./styles/UserSearchPage.css";

// USER SEARCH
function UserSearchPage() {
  const [userId, setUserId] = useState(""); // For user input
  const [user, setUser] = useState(null); // For storing user details
  const [error, setError] = useState(""); // For error messaging

  // Handle search
  const handleSearch = async () => {
    if (!userId) {
      // Invalid userId
      setError("Please enter a valid User ID.");
      setUser(null);
      return;
    }

    try {
      setError(""); // Clear previous errors
      const response = await axios.get(`${baseURL}/user_search/${userId}`);
      setUser(response.data); // Set user data
    } catch (err) {
      setUser(null); // Clear user data
      setError(err.response?.data?.description || "User not found.");
    }
  };

  return (
    <div className="user-search-container">
      <img src={animalGuy}/>
      <h1>User Search</h1>
      <div className="search-box">
        {/* Input ID Field and Search Button */}
        <label htmlFor="userId">Enter User ID:</label>
        <div className="input-actions">
          <input
            type="text"
            id="userId"
            value={userId}
            placeholder="Enter User ID (e.g. 2)"
            onChange={(e) => setUserId(e.target.value)}
          />
          <button onClick={handleSearch}>Search</button>
        </div>

        {/* Display user details if found */}
        {user && (
          <div className="user-found">
            <p>User Found!</p>
            <p>
              <strong>Name:</strong> {user.name}
            </p>
            <p>
              <strong>UID:</strong> {user.user_id}
            </p>
            <Link to={`/user/${user.user_id}`}>Go to User Page</Link>
          </div>
        )}

        {/* Display error if user not found */}
        {error && <div className="error-message">{error}</div>}
      </div>
    </div>
  );
}

export default UserSearchPage;
