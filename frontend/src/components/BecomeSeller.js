// IMPORTS
import React from "react";
import { useNavigate } from "react-router-dom";

import "./styles/Account/BecomeSeller.css";

// BECOME A SELLER Component (Account Page)
const BecomeSeller = () => {
  // Initialize React Router navigation 
  const navigate = useNavigate();

  return (
    <div className="become-seller-container">
      <h2>Become a Seller</h2>
      <p>
        Join our platform as a seller to manage your inventory, orders, and
        more!
      </p>
      {/* Navigate to the Add Product screen on button click */}
      <button onClick={() => navigate("/add_product")}>Get Started Today</button>
    </div>
  );
};

export default BecomeSeller;
