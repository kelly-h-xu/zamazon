// IMPORTS
import React, { useEffect, useState } from "react";
import axios from "axios"; 
import { useLocation } from "react-router-dom";

import BecomeSeller from "./BecomeSeller";
import Fulfilled from "./FulfilledOrders";
import Inventory from "./Inventory";
import ProfileInfo from "./ProfileInformation";
import ProtectedPage from "./ProtectedPage";
import PurchaseHistory from "./PurchaseHistory";
import SocialCenter from "./Social/SocialCenter";
import Unfulfilled from "./UnfulfilledOrders";
import { baseURL } from "../config";

import "./styles/Account/AccountPage.css";

// ACCOUNT PAGE
const AccountPage = () => {
  const location = useLocation();
  const [activeTab, setActiveTab] = useState("profile");
  const [isSeller, setIsSeller] = useState(false); // State to track seller status

  // Fetch seller status from 8080
  useEffect(() => {
    const fetchSellerStatus = async () => {
      try {
        const response = await axios.get(`${baseURL}/is_seller`, {
          withCredentials: true,
        });
        setIsSeller(response.data.seller_status); // Set the seller status
      } catch (error) {
        console.error("Error fetching seller status:", error);
      }
    };

    fetchSellerStatus();
  }, []);

  // Check for active account tab in location state
  useEffect(() => {
    if (location.state && location.state.activeTab) {
      setActiveTab(location.state.activeTab);
    }
  }, [location]);

  return (
    <ProtectedPage>
      <div className="account-container">
        <h1>My Account</h1>
        <div className="account-flex">
          <div className="account-col1">
            {/* Profile tab list */}
            <ul>
              <li
                className={activeTab === "profile" ? "active" : ""}
                onClick={() => setActiveTab("profile")}
              >
                Profile Information
              </li>
              <li
                className={activeTab === "history" ? "active" : ""}
                onClick={() => setActiveTab("history")}
              >
                Purchase History
              </li>
              <li
                className={activeTab === "social" ? "active" : ""}
                onClick={() => setActiveTab("social")}
              >
                Social Center
              </li>
              {/* Check if the user is a seller to conditionally display */}
              {/* Inventory and Fulfilment tabs */}
              {isSeller ? (
                <>
                  <li
                    className={activeTab === "inventory" ? "active" : ""}
                    onClick={() => setActiveTab("inventory")}
                  >
                    Inventory
                  </li>
                  <li
                    className={activeTab === "unfulfilled" ? "active" : ""}
                    onClick={() => setActiveTab("unfulfilled")}
                  >
                    Unfulfilled Orders
                  </li>
                  <li
                    className={activeTab === "fulfilled" ? "active" : ""}
                    onClick={() => setActiveTab("fulfilled")}
                  >
                    Fulfilled Orders
                  </li>
                </>
              ) : (
                // Else display a Become a Seller tab
                <li
                  className={activeTab === "become-seller" ? "active" : ""}
                  onClick={() => setActiveTab("become-seller")}
                >
                  Become a Seller
                </li>
              )}
            </ul>
          </div>
          {/* Load in the appropriate component */}
          <div className="account-col2">
            {activeTab === "profile" && <ProfileInfo />}
            {activeTab === "history" && <PurchaseHistory />}
            {activeTab === "social" && <SocialCenter />}
            {activeTab === "inventory" && isSeller && <Inventory />}
            {activeTab === "unfulfilled" && isSeller && <Unfulfilled />}
            {activeTab === "fulfilled" && isSeller && <Fulfilled />}
            {activeTab === "become-seller" && !isSeller && <BecomeSeller/>}
          </div>
        </div>
      </div>
    </ProtectedPage>
  );
};

export default AccountPage;
