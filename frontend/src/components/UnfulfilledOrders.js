// IMPORTS
import React, { useEffect, useState, useCallback } from "react";
import {Link} from "react-router-dom";
import axios from "axios";
import Popup from "reactjs-popup";

import Pagination from "@mui/material/Pagination";
import ProtectedPage from "./ProtectedPage";
import { baseURL } from "../config";

import "./styles/Account/InventoryPagination.css";
import "./styles/Account/Orders.css";
import "reactjs-popup/dist/index.css";

// UNFULFILLED ORDERS Component (Account Page)
function Unfulfilled() {
  const [unfulfilledOrders, setUnfulfilledOrders] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  // Use 2 items per page
  const itemsPerPage = 2;
  const [totalItems, setTotalItems] = useState(0)

  // Fetch Order Data from 8080
  const fetchOrderData = useCallback(async () => {
    try {
      const response = await axios.get(`${baseURL}/get_unfulfilled_ordered_items?currentPage=${currentPage}&itemsPerPage=${itemsPerPage}`, {
        withCredentials: true,
      });
      // Set Unfilfilled Orders as the response
      setUnfulfilledOrders(response.data.unfulfilled);
      setTotalItems(response.data.total)
      console.log(totalItems)
    } catch (error) {
      // Error messaging
      console.error("Error fetching orders data:", error);
    }
  }, [itemsPerPage, currentPage]);

  useEffect(() => {
    fetchOrderData();
  }, [fetchOrderData]);

  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const [purchase_id, setPurchaseId] = useState("");
  const [product_id, setProductId] = useState("");

  const handleClick = (prod_id, purch_id) => {
    setProductId(prod_id);
    setPurchaseId(purch_id);
    // console.log(product_id, purchase_id)
  };

  // Fulfill clicked item on the backend
  const handleSubmit = async (event) => {
    event.preventDefault();
    fetch(`${baseURL}/fulfill_item`, {
      method: "POST",
      credentials: "include", // ensure cookies are sent
      body: JSON.stringify({
        product_id: product_id,
        purchase_id: purchase_id,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    fetchOrderData();
  };

  return (
    // Ensure Users are logged in
    <ProtectedPage>
      <div className="order-container">
        {totalItems === 0 ? (
          // No unfulfilled orders
          <p>No unfulfilled orders.</p>
        ) : (
          // If unfulfilled orders, display them
          <div className="display">
            <ul className="product-list">
              {unfulfilledOrders.map((product) => (
                <li key={product.product_id} className="product-card">
                  {/* All details for a product in an unfulfilled order */}
                  <div className="product-details">
                  <Link
                    to={`/product/${encodeURIComponent(product.name)}`}
                    state={{ product_name: product.name }}
                  >
                    {product.name}
                    </Link>
                    <p>
                      <strong>Product ID:</strong> {product.product_id}
                    </p>
                    <p>
                      <strong>Order ID:</strong> {product.purchase_id}{" "}
                    </p>
                    <p>
                      <strong>Category:</strong> {product.category}
                    </p>
                    <p>
                      <strong>Price at Purchase:</strong> ${product.at_price}
                    </p>
                    <p>
                      <strong>Quantity Purchased:</strong>{" "}
                      {product.order_quantity}
                    </p>
                    {/* <p>{product.description}</p> */}
                    <p>Deliver To {product.address}</p>
                    <p className="date-time">Ordered on {product.date_time}</p>
                    {/* Popup for order fulfillment confirmation */}
                    <Popup
                      onClose={fetchOrderData}
                      trigger={
                        <button
                          className="inventory-container-button"
                          type="button"
                        >
                          Fulfill Order
                        </button>
                      }
                    >
                      {/* Confirmation popup, close on cancel */}
                      {(closePopup) => (
                        <form method="post" onSubmit={handleSubmit}>
                          <p style={{marginTop: "0"}}>Are you sure you'd like to fulfill this order?</p>
                          <div
                            className="popup-buttons"
                            style={{
                              display: "flex",
                              flexDirection: "row",
                              justifyContent: "space-between",
                            }}
                          >
                            <button
                              className="inventory-container-button"
                              onClick={() =>
                                handleClick(
                                  product.product_id,
                                  product.purchase_id
                                )
                              }
                              type="submit"
                            >
                              Yes
                            </button>
                            <button
                              className="inventory-container-button"
                              type="button"
                              onClick={() => closePopup()}
                              style = {{backgroundColor: "#a14141"}}
                            >
                              Cancel
                            </button>
                          </div>
                        </form>
                      )}
                    </Popup>
                  </div>
                </li>
              ))}
            </ul>
            {/* Pagination controls */}
            <div className="pagination">
              <Pagination
                count={totalPages}
                page={currentPage}
                onChange={(event, page) => setCurrentPage(page)}
                shape="rounded"
                sx={{ backgroundColor: "transparent" }}
              />
            </div>
          </div>
        )}
      </div>
    </ProtectedPage>
  );
}

export default Unfulfilled;
