// IMPORTS
import React, { useState, useContext } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "./AuthContext";
import { baseURL } from "../config";

import "./styles/LoginPage.css";

// LOGIN
const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState({});
  const [flashMessage, setFlashMessage] = useState("");
  const navigate = useNavigate();
  const { setAuthStatus } = useContext(AuthContext);

  // Handle login submit button
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setFlashMessage("");

    try {
      const response = await axios.post(
        `${baseURL}/login`,
        {
          email: email,
          password: password,
        },
        { withCredentials: true }
      );

      // Redirect to a different page after successful login
      if (response.status === 200) {
        setAuthStatus(true);
        navigate("/");
      }
    } catch (err) {
      // Handle form validation errors and flash messages
      if (err.response && err.response.status === 400) {
        setErrors(err.response.data.errors || {});
        setFlashMessage(err.response.data.message || "");
      } else {
        setFlashMessage("An error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="login-container">
      <h1>Login</h1>
      <form onSubmit={handleSubmit} className="login-form">
        {/* Link to Registration */}
        <a className="register-link" href="/register" role="button">
          New to Zamazon? Register here!
        </a>

        {/* Email Field */}
        <div>
          <input
            type="email"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email here"
            size="32"
            required
          />
          {errors.email && (
            <span style={{ color: "red" }}>[{errors.email}]</span>
          )}
        </div>

        {/* Password Field */}
        <div>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password here"
            size="32"
            required
          />
          {errors.password && (
            <span style={{ color: "red" }}>[{errors.password}]</span>
          )}
        </div>

        {/* Flash Messages */}
        {flashMessage && (
          <div>
            <span style={{ color: "red" }}>{flashMessage}</span>
          </div>
        )}

        {/* Submit Button */}
        <button type="submit" className="btn btn-black">
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
