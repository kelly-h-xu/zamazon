import React from "react";
import { useState, useCallback, useContext } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import { baseURL } from "../../config";
import { AuthContext } from "../AuthContext";

import "../styles/Products/ProductCard.css";

function ProductListing({ listing }) {
  const { isAuthenticated } = useContext(AuthContext);
  const {
    product_id,
    product_name,
    seller_id,
    seller_name,
    price,
    quantity,
    active,
  } = listing;

  console.log(listing);

  const [items, setItems] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);
  // todo: move the functions messing w the cart to a hook and use that later.
  // works as wanted for now
  const fetchCartItems = useCallback(async () => {
    try {
      const response = await axios.get(`${baseURL}/carts`, {
        withCredentials: true,
      }); //the route defined in your backend view. Make sure to set the withCredentials to true in all api requests
      setItems(response.data.items || []);
      setTotalPrice(response.data.total_price || 0);
    } catch (error) {
      console.error("Failed to fetch cart items:", error);
    }
  }, []);

  const addItemToCart = async (product_id) => {
    const response = await axios.post(
      `${baseURL}/add-to-cart/${product_id}`,
      {},
      {
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      }
    );
    if (response.status === 200) {
      // fetch the updated carts items immediately after updating the cart
      fetchCartItems();
    } else {
      console.error("Failed to add quantity");
    }
  };

  return (
    <div className="listing-card">
      <div className="col1">
        <Link to={`/user/${encodeURIComponent(listing.seller_id)}`}>
          <h3>{seller_name}</h3>
        </Link>
        {quantity > 0 && <h4>{quantity} left in stock</h4>}
        <h4>${price}</h4>
      </div>
      {quantity === 0 ? (
        <p>Sold Out</p> // Display "Sold Out" when quantity is 0
      ) : isAuthenticated ? (
        <button
          className="add-to-cart-button"
          onClick={() => addItemToCart(product_id)}
        >
          Add to Cart
        </button>
      ) : (
        <Link to="/login" className="login-to-purchase">
          Login to purchase
        </Link>
      )}
    </div>
  );
}
export default ProductListing;
