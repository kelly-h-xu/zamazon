// IMPORTS
import React from "react";
import { NavLink } from "react-router-dom";

import "./styles/Navbar.css";

// PRODUCT NAVBAR
function ProductNavbar() {
  return (
    <nav className="nav-container product-nav-container">
      <ul>
        {/*  Links to all product categories*/}
        <li>
          <NavLink
            to="products/all"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            All Plants
          </NavLink>
        </li>
        <li>
          <NavLink
            to="products/flowers"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Flowers
          </NavLink>
        </li>
        <li>
          <NavLink
            to="products/succulents"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Succulents
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/products/herbs"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Herbs
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/products/fruit-veg"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Fruits and Vegetables
          </NavLink>
        </li>
      </ul>
    </nav>
  );
}
export default ProductNavbar;
