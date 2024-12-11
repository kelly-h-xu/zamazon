// IMPORTS
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

import ProtectedPage from "./ProtectedPage";
import { baseURL } from "../config";

import "./styles/UpdateProduct.css";
import "reactjs-popup/dist/index.css";

// UPDATE PRODUCT Page
function UpdateProduct() {
  const [product_name, setProductName] = useState("");
  const [description, setDescription] = useState("");
  const [image_url, setImageUrl] = useState("");
  const [category, setCategory] = useState("");
  const navigate = useNavigate();

  const location = useLocation();

  useEffect(() => {
    if (location.state && location.state.product_name) {
      setProductName(location.state.product_name);
    }
    if (location.state && location.state.description) {
      setDescription(location.state.description);
    }
    if (location.state && location.state.image_url) {
      setImageUrl(location.state.image_url);
    }
    if (location.state && location.state.category) {
      setCategory(location.state.category);
    }
  }, [location]);

  // Route to inventory
  const goToInventory = () => {
    navigate("/account", { state: { activeTab: "inventory" } });
  };

  // Handle update product in the backend
  const handleSubmit = async (event) => {
    event.preventDefault();
    const x = await fetch(`${baseURL}/update_catalog`, {
      method: "POST",
      credentials: "include", // Ensures cookies are sent
      body: JSON.stringify({
        product_name: product_name,
        description: description,
        category: category,
        image_url: image_url,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Route to the inventory
    goToInventory();
  };

  return (
    // Ensure user is logged in
    <ProtectedPage>
      <div className="update-form-container">
        <h2>{product_name}</h2>
        {/* Warning */}
        <p>Note: product names cannot be changed after creation.</p>
        {/* Seller input all updated fields */}
        <form onSubmit={handleSubmit}>
          <ul>
            <li>
              <label>
                Item Description <br />
                <textarea
                  id="description"
                  type="text"
                  value={description}
                  required
                  onChange={(e) => setDescription(e.target.value)}
                ></textarea>
              </label>
            </li>
            <li>
              <label>
                Category <br />
                {/* Drop down for category */}
                <select
                  id="category"
                  required
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                >
                  <option value="">Select</option>
                  <option value="Flowers">Flowers</option>
                  <option value="Succulents">Succulents</option>
                  <option value="Herbs">Herbs</option>
                  <option value="Fruits and Vegetables">
                    Fruits and Vegetables
                  </option>
                </select>
              </label>
            </li>
            <li>
              <label>
                Image URL <br />
                <input
                  id="image_url"
                  type="text"
                  value={image_url}
                  required
                  onChange={(e) => setImageUrl(e.target.value)}
                ></input>
              </label>
            </li>
          </ul>
          {/* Submit update or return to Inventory */}
          <div className="update-form-button-container">
            <button className="update" type="submit">
              Update Item
            </button>
            <button className="cancel" onClick={goToInventory}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </ProtectedPage>
  );
}
export default UpdateProduct;
