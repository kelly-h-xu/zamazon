// IMPORTS
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import ProtectedPage from "./ProtectedPage";
import { baseURL } from "../config";

import "./styles/AddProduct.css";

// ADD PRODUCT
function AddProduct() {
  const [name, setName] = useState("");
  const [verified, setVerified] = useState(true);
  const [description, setDescription] = useState("");
  const [image_url, setImageUrl] = useState("");
  const [price, setPrice] = useState(0);
  const [quantity, setQuantity] = useState(0);
  const [category, setCategory] = useState("");
  const navigate = useNavigate();

  // Handle the product name change in the dtaabase
  const handleNameChange = async (product_name) => {
    setName(product_name);

    try {
      // Product listing has not yet been created
      const response = await fetch(`${baseURL}/check_availability`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ product_name }),
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();

      setVerified(data.availability);

      if (!data.availability) {
        // Pull data from the creator listing
        setDescription(data.description);
        setImageUrl(data.image_url);
        setCategory(data.category);
        document.getElementById("description").value = data.description;
        document.getElementById("image_url").value = data.image_url;
        document.getElementById("category").value = data.category;
      } else {
        // Use blank placeholders 
        setDescription("");
        setImageUrl("");
        setCategory("");
      }
    } catch (error) {
      // Error messaging
      console.error("Error in handleNameChange:", error);
    }
  };

  // Handle submitting the listing in the backend
  const handleSubmit = async (event) => {
    event.preventDefault();
    if (verified) {
      await fetch(`${baseURL}/add_to_catalog`, {
        // Add product to catalog
        method: "POST",
        credentials: "include",
        body: JSON.stringify({
          product_name: name,
          description,
          category,
          image_url,
        }),
        headers: { "Content-Type": "application/json" },
      });
    }
    if (price && quantity) {
      // Add product to seller inventory
      await fetch(`${baseURL}/add_to_inventory`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ product_name: name, price, quantity }),
        headers: { "Content-Type": "application/json" },
      });
    }
    // Navigate to the inventory
    navigate("/account", { state: { activeTab: "inventory" } });
  };

  return (
    // User must be logged in
    <ProtectedPage>
      <div className="add-product-container">
        <h1>Add Product</h1>
        <form onSubmit={handleSubmit}>
          <ul>
            <li>
              <label>
                Item Name <br />
                <input
                  type="text"
                  value={name}
                  required
                  onChange={(e) => handleNameChange(e.target.value)}
                />
              </label>
            </li>
            {verified && (
              <>
                <li>
                  <label>
                    Item Description <br />
                    <textarea
                      id="item-add-prod-description"
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
                      <option value="Fruits and Vegetables">Fruits and Vegetables</option>
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
                    />
                  </label>
                </li>
              </>
            )}
            <li>
              <label>
                Price <br />
                <input
                  id="price"
                  value={price}
                  type="number"
                  min=".00"
                  step=".01"
                  onChange={(e) => setPrice(e.target.value)}
                />
              </label>
            </li>
            <li>
              <label>
                Available Quantity <br />
                <input
                  id="quantity"
                  type="number"
                  min="0"
                  step="1"
                  value={quantity}
                  onChange={(e) => setQuantity(e.target.value)}
                />
              </label>
            </li>
          </ul>
          <div className = "add-prod-button-container">
            <button className="submit-button" type="submit">
                Create Item
            </button>
            <button className="back-button" onClick={() => navigate("/account")}>
                Cancel
            </button>
          </div>
        </form>
      </div>
    </ProtectedPage>
  );
}

export default AddProduct;
