// IMPORTS
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams, Link } from "react-router-dom";

import MyProductReview from "../components/Social/MyProductReview";
import MySellerReview from "../components/Social/MySellerReview";
import ProtectedPage from "./ProtectedPage";
import { baseURL } from "../config";

import "./styles/OrderDetails.css";

// ORDER DETAILS
const OrderDetails = () => {
  const [items, setItems] = useState([]);
  const { purchaseID } = useParams();

  // Get the order details from 8080
  const fetchOrderDetails = async () => {
    try {
      const response = await axios.get(
        `${baseURL}/buys-by-order/${purchaseID}`,
        { withCredentials: true }
      );
      // Set the details as the response or an empty array
      setItems(response.data.items || []);
    } catch (error) {
      // Error messaging
      console.error("Error fetching order details:", error);
    }
  };

  useEffect(() => {
    fetchOrderDetails();
  }, [purchaseID]);

  // Calculate the total cost, purchase date, and fulfillment status
  const totalCost =
    items.length > 0 ? Math.abs(items[0].at_balance).toFixed(2) : null;
  const purchaseDate = items.length > 0 ? items[0].purchase_date : null;
  const orderFulfillmentStatus =
    items.length > 0 ? items[0].fulfillment_status : null;

  return (
    // Require users be logged in
    <ProtectedPage>
      <div className="order-details-container">
        <h2 className="order-title">Order Details</h2>

        {/* Summary details for the order */}
        <div className="order-summary">
          <p>
            <strong>Ordered On:</strong>{" "}
            <span className="date-time">{purchaseDate}</span>
          </p>
          <p>
            <strong>Order #:</strong> {purchaseID}
          </p>
          <p>
            <strong>Grand Total:</strong> ${totalCost}
          </p>
          <p>
            <strong>Order Fulfillment Status:</strong>{" "}
            <span
              className={`order-fulfillment-status ${
                orderFulfillmentStatus ? "fulfilled" : "not-fulfilled"
              }`}
            >
              {orderFulfillmentStatus ? "Fulfilled :)" : "Not Fulfilled"}
            </span>
          </p>
        </div>

        {/* List of items in the order */}
        <div className="order-items">
          {items.map((item) => (
            // Col1: Item image
            <div key={item.product_id} className="order-item">
              <div className="col1">
                <img
                  src={item.image_url}
                  className="item-image"
                  alt={item.product_name}
                />
              </div>
              {/* Col 2: Item name and fulfillment status */}
              <div className="col2">
                <div className="item-info">
                  <h3 className="item-name">
                    <Link
                      to={`/product/${encodeURIComponent(item.product_name)}`}
                      state={{ product_name: item.product_name }}
                    >
                      {item.product_name}
                    </Link>{" "}
                    x{item.quantity}
                  </h3>
                  <p>${item.price_at_purchase}/Unit</p>
                </div>
                <div
                  className={`fulfillment-status ${
                    item.fulfillment_time ? "fulfilled" : "to-be-fulfilled"
                  }`}
                >
                  {item.fulfillment_time
                    ? `Fulfilled On: ${item.fulfillment_time}`
                    : "To Be Fulfilled"}
                </div>
              </div>
              {/* Col3: User's Product Review */}
              <div className="col3">
                <MyProductReview id="col3" productName={item.product_name} />
              </div>
              {/* Col3: User's Seller Review */}
              <div className="col4">
                <MySellerReview
                  id="col4"
                  sellerId={item.seller_id}
                  sellerName={item.seller_name}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </ProtectedPage>
  );
};

export default OrderDetails;
