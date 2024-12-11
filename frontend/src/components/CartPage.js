// IMPORTS
import React, { useEffect } from "react";
import { useState } from "react";
import { useCallback } from "react";
import axios from "axios";

import Pagination from "@mui/material/Pagination";
import ProtectedPage from "./ProtectedPage";
import { baseURL } from "../config";

import "./styles/CartPage.css";

// CART PAGE
const CartPage = () => {
  const [items, setItems] = useState([]);
  const [totalPrice, setTotalPrice] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const itemsPerPage = 5;

  // Get the paginated cart items from the 8080 backend
  const fetchPaginatedCartItems = useCallback(async () => {
    try {
      const response = await axios.get(
        `${baseURL}/get-paginated-carts?page=${currentPage}&itemsPerPage=${itemsPerPage}`,
        { withCredentials: true }
      );
      // Set the data based on the response
      setItems(response.data.items || []); // Emtpy array by default
      setTotalPrice(response.data.total_price || 0); // 0 by default
      setTotalPages(response.data.total_pages || 1); // 1 by default
    } catch (error) {
      // Error messaging
      console.error("Failed to fetch cart items:", error);
    }
  }, [currentPage, itemsPerPage]);

  useEffect(() => {
    fetchPaginatedCartItems();
  }, [fetchPaginatedCartItems]);

  // Handle adding an item to cart in the database
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
      // Fetch the updated carts items
      fetchPaginatedCartItems();
    } else {
      // Error messaging
      console.error("Failed to add quantity");
    }
  };

  // Handle decreasing an item quantity in the databse
  const decreaseQuantity = async (product_id) => {
    const response = await axios.patch(
      `${baseURL}/decrease-quantity/${product_id}`,
      {},
      { withCredentials: true }
    );
    if (response.status === 200) {
      fetchPaginatedCartItems();
    } else {
      // Error messaging
      console.error("Failed to decrease quantity");
    }
  };

  // Handle removing an item from the cart in the database
  const removeItemFromCart = async (product_id) => {
    const response = await axios.delete(
      `${baseURL}/delete-item/${product_id}`,
      { withCredentials: true }
    );
    if (response.status === 200) {
      fetchPaginatedCartItems();
      // Adjust the page if deletion causes issues
      if (items.length === 1 && currentPage > 1) {
        setCurrentPage((prevPage) => prevPage - 1);
      }
    } else {
      // Error messaging
      console.error("Failed to remove item from cart");
    }
  };

  // Handle clearing the cart in the database
  const clearCart = async () => {
    const response = await axios.delete(`${baseURL}/clear-cart`, {
      withCredentials: true,
    });
    if (response.status === 200) {
      fetchPaginatedCartItems();
    } else {
      // Error messaging
      console.error("Could not clear cart :(");
    }
  };

  // Handle placing an order in the backend
  const submitOrder = async () => {
    try {
      const response = await axios.post(
        `${baseURL}/place-order`,
        {},
        {
          withCredentials: true,
          headers: { "Content-Type": "application/json" },
        }
      );

      if (response.status === 200) {
        // Successfully placed order
        const { purchase_id, date_time } = response.data;
        alert(
          `Order submitted successfully!\nPurchase ID: ${purchase_id}\nDate: ${new Date(
            date_time
          ).toLocaleString()}`
        );
        fetchPaginatedCartItems(); // Refresh the cart to reflect the cleared state
      } else {
        alert("Failed to place order. Please try again.");
      }
    } catch (error) {
      // Erorr messaging
      if (error.response) {
        const errorMessage =
          error.response.data?.error || "Unknown error occurred.";
        alert(`Error placing order: ${errorMessage}`);
      } else {
        alert("Network error. Please try again later.");
      }
    }
  };

  return (
    // Check user is logged
    <ProtectedPage>
      <div className="cart-container">
        {/* Check the cart has items */}
        {items.length === 0 ? (
          <p className="empty-cart-message">No Items in Cart </p>
        ) : (
          // Render  cart items
          <div>
            <div className="cart-header">
              <h1>Your Cart Items</h1>
              <h3>Total Price: ${totalPrice}</h3>
              <div className="overall-cart-buttons">
                {/* Button to clear the cart */}
                <button
                  className="cart-button"
                  onClick={() => {
                    if (
                      window.confirm("Are you sure you want to clear the cart?")
                    ) {
                      clearCart();
                    }
                  }}
                >
                  Clear Cart
                </button>
                {/* Button to submit an order, "checkout" */}
                <button
                  className="cart-button"
                  onClick={() => {
                    submitOrder();
                  }}
                >
                  {" "}
                  Submit Order{" "}
                </button>
              </div>
            </div>

            <div>
              {/* List of products in a user's cart */}
              <ul className="product-list">
                {items.map((item) => (
                  <li key={item.product_id} className="product-card">
                    <div className="product-details">
                      {item.image_url ? (
                        <img src={item.image_url} className="product-image" />
                      ) : (
                        <div className="product-image no-image">No image</div>
                      )}
                      <div className="product-info">
                        <h4>{item.product_name}</h4>
                        <p>Price: ${item.at_price}</p>
                        <p>Seller ID: {item.seller_id}</p>
                      </div>
                      {/* Buttons to change quantity */}
                      <div className="quantity-container">
                        <div className="quantity-controls">
                          <button
                            onClick={() => decreaseQuantity(item.product_id)}
                          >
                            -
                          </button>
                          <span>{item.quantity}</span>
                          <button
                            onClick={() => addItemToCart(item.product_id)}
                          >
                            +
                          </button>
                        </div>
                        {/* Button to remove the item */}
                        <button
                          className="delete-button"
                          onClick={() => removeItemFromCart(item.product_id)}
                        >
                          🗑️
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
            {/* Pagination controls */}
            <Pagination
              count={totalPages}
              page={currentPage}
              onChange={(event, page) => setCurrentPage(page)}
              shape="rounded"
              color="primary"
            />
          </div>
        )}
      </div>
    </ProtectedPage>
  );
};

export default CartPage;
