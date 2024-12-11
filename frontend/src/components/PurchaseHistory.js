// IMPORTS 
import React, { useState, useCallback, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import Pagination from "@mui/material/Pagination";
import { baseURL } from "../config";

import "./styles/Account/PurchaseHistory.css";
import "./styles/Socials/SocialPagination.css";

// PURCHASE HISTORY Component (Account Page)
function PurchaseHistory() {
  const [purchases, setPurchases] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [sortBy, setSortBy] = useState("date_time"); // Default sort by date_time
  const itemsPerPage = 3;

  // Fetch purchases with pagination and sorting
  const fetchPurchases = useCallback(async () => {
    try {
      const response = await axios.get(
        `${baseURL}/purchase_history?page=${currentPage}&items_per_page=${itemsPerPage}&sort_by=${sortBy}`,
        {
          withCredentials: true,
        }
      );

      // console.log(response.data); // Debug response structure
      setPurchases(response.data.purchases || []);
      setTotalPages(response.data.total_pages || 1);
    } catch (error) {
      console.error("Error fetching purchase history:", error);
    }
  }, [currentPage, itemsPerPage, sortBy]);

  useEffect(() => {
    fetchPurchases();
  }, [fetchPurchases]);

  // Handle sort change
  const handleSortChange = (event) => {
    setSortBy(event.target.value);
    setCurrentPage(1); // Reset to page 1 when sorting changes
  };

  return (
    <div className="purchase-history-container">
      <div className="sort-container">
        <label htmlFor="sort">Sort By:</label>
        <select id="sort" value={sortBy} onChange={handleSortChange}>
          <option value="date_time">Date</option>
          <option value="total_amount">Total Amount</option>
          <option value="number_of_items">Number of Items</option>
        </select>
      </div>
      {purchases.length === 0 ? (
        <p>No purchases made yet.</p>
      ) : (
        purchases.map((purchase) => (
          <div className="purchase-card" key={purchase.order_id}>
            <h2>
              <span>Order ID:</span>
              <Link to={`/order/${purchase.order_id}`}>
                {purchase.order_id}
              </Link>
            </h2>
            <p className="detail price">Total Cost: ${purchase.total_amount}</p>
            <p className="detail fulfillment">
              Fulfillment Status:{" "}
              <span
                className={
                  purchase.fulfillment_status ? "completed" : "pending"
                }
              >
                {purchase.fulfillment_status ? "Completed" : "Pending"}
              </span>
            </p>
            <p className="detail">
              Number of Items: {purchase.number_of_items}
            </p>
            <p className="date-time">
              Purchased on {new Date(purchase.purchase_date).toLocaleString()}
            </p>
          </div>
        ))
      )}
      <div className="pagination">
        <Pagination
          count={totalPages}
          page={currentPage}
          onChange={(event, value) => setCurrentPage(value)}
          shape="rounded"
          className="pagination"
        />
      </div>
    </div>
  );
}

export default PurchaseHistory;
