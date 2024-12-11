import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Import useNavigate from React Router

import { baseURL } from "../config";

import "./styles/Register.css";

// REGISTRATION PAGE
const Register = () => {
  const [firstname, setFirstname] = useState("");
  const [lastname, setLastname] = useState("");
  const [email, setEmail] = useState("");
  const [address, setAddress] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate(); // Initialize useNavigate

  // Register a new user on the backend 
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check password fields match
    if (password !== confirmPassword) {
      setMessage("Error: Passwords do not match.");
      return;
    }

    const userData = {
      firstname,
      lastname,
      email,
      address,
      password,
    };

    try {
      const response = await axios.post(`${baseURL}/register`, userData);
      setMessage(response.data.message);

      if (response.status === 201) {
        // Redirect to /login on successful registration
        navigate("/login");
      }
    } catch (error) {
      // Error messaging
      if (error.response) {
        setMessage(error.response.data.message);
      } else {
        setMessage("An error occurred while processing your request.");
      }
    }
  };

  return (
    <div className="register-container">
      <h1>Register</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="First Name"
          value={firstname}
          onChange={(e) => setFirstname(e.target.value)}
        />
        <input
          type="text"
          placeholder="Last Name"
          value={lastname}
          onChange={(e) => setLastname(e.target.value)}
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="text"
          placeholder="Address"
          value={address}
          onChange={(e) => setAddress(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        <button type="submit">Register</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default Register;
