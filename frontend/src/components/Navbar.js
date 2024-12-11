// IMPORTS
import React, { useContext } from "react";
import { IoMdCart } from "react-icons/io";
import { IoPersonCircleSharp } from "react-icons/io5";
import { PiAddressBookFill } from "react-icons/pi";
import { PiAcornFill } from "react-icons/pi";
import { TbLogout } from "react-icons/tb";
import { TbLogin } from "react-icons/tb";
import { NavLink, useNavigate } from "react-router-dom";

import { AuthContext } from "./AuthContext";

import "./styles/Navbar.css";

// NAVBAR
function Navbar() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  // Redirect to the home page on logout
  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="nav-container">
      {/* Links to home, account, cart, user search, and login/logout */}
      <ul>
        <NavLink className="nav-item center-item" to="/">
          <PiAcornFill size={24} />
          Zamazon
        </NavLink>

        <li className="nav-item">
          <NavLink
            to="/users"
            className={({ isActive }) => (isActive ? "current" : "")}
          >
            <PiAddressBookFill size={24} />
          </NavLink>
        </li>
        {/* Replacing My Account and Shopping Cart with icons */}
        <li className="nav-item">
          <NavLink
            to="/account"
            className={({ isActive }) => (isActive ? "current" : "")}
          >
            <IoPersonCircleSharp size={24} /> {/* User icon */}
          </NavLink>
        </li>
        <li className="nav-item">
          <NavLink
            to="/cart"
            className={({ isActive }) => (isActive ? "current" : "")}
          >
            <IoMdCart size={24} /> {/* Shopping Cart icon */}
          </NavLink>
        </li>

        {/* Toggle login/logout text and routing */}
        {isAuthenticated ? (
          <li className="nav-item">
            <NavLink to="/" onClick={handleLogout} id="logout">
              <TbLogout size={24} />
            </NavLink>
          </li>
        ) : (
          <li className="nav-item">
            <NavLink to="/login">
              <TbLogin size={24} />
            </NavLink>
          </li>
        )}
      </ul>
    </nav>
  );
}

export default Navbar;
