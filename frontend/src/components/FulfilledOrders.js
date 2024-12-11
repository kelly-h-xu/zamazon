// IMPORTS
import React, { useEffect, useState, useCallback } from "react";
import {Link} from "react-router-dom";
import axios from "axios";

import Pagination from "@mui/material/Pagination";
import ProtectedPage from "./ProtectedPage";
import { baseURL } from "../config";

import "./styles/Account/Inventory.css";
import "./styles/Account/InventoryPagination.css";

// FULFILLED ORDERS Component (Account Page)
function Fulfilled() {
  const [fulfilledOrders, setFulfilledOrders] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 2;
  const [totalItems, setTotalItems] = useState(0)

  // Fetch order data from 8080 backend
  const fetchOrderData = useCallback(async () => {
    try {
      const response = await axios.get(`${baseURL}/get_fulfilled_ordered_items?currentPage=${currentPage}&itemsPerPage=${itemsPerPage}`, {
        withCredentials: true,
      });
      // Set the fulfilled orders as the response
      setFulfilledOrders(response.data.fulfilled);
      setTotalItems(response.data.total)
    } catch (error) {
      console.error("Error fetching orders data:", error);
    }
  }, [totalItems, currentPage]);

  useEffect(() => {
    fetchOrderData();
  }, [fetchOrderData]);

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  // HTML Return
  return (
    <ProtectedPage>
      <div className="order-container">
        {/* Check if the seller has fulfilled orders */}
        {totalPages === 0 ? (
          <p>No orders.</p>
        ) : (
          // If they do display the list
          <div className="display">
            <ul className="product-list">
              {fulfilledOrders.map((product) => (
                <li key={product.product_id} className="product-card">
                  {/* Display the product details by product */}
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
                      <strong>Quantity Purchased:</strong>
                      {product.order_quantity}
                    </p>
                    <p>
                      <strong>Quantity in Stock:</strong>
                      {product.product_quantity}
                    </p>
                    {/* <p>{product.description}</p> */}
                    <p className="date-time">Ordered on {product.date_time}</p>
                    <p className="date-time">
                      Fulfilled On {product.fulfillment_time}
                    </p>
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
                // color="primary"
                sx={{ backgroundColor: "transparent" }}
              />
            </div>
          </div>
        )}
      </div>
    </ProtectedPage>
  );
}

export default Fulfilled;
