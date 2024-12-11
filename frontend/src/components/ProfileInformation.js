// IMPORTS
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

import pencil from "../assets/edit_pencil.png";
import { baseURL } from "../config";

import "./styles/Account/ProfileInformation.css";

// PROFILE INFO Component (Account Page)
const ProfileInfo = () => {
  const [user, setUser] = useState({});
  const [editingField, setEditingField] = useState(null); // which field is being edited
  const [editValue, setEditValue] = useState("");
  const [passEdit, setPassEdit] = useState({
    newPassword: "",
    confirmPassword: "",
  });
  const [transactionAmount, setTransactionAmount] = useState("");
  const [showTransactionInput, setShowTransactionInput] = useState(false);
  const [transactionSource, setTransactionSource] = useState("");
  const [transactionType, setTransactionType] = useState(""); // "withdraw" or "deposit"
  const [showConfirmation, setShowConfirmation] = useState(false); // To show confirmation message

  // Get a user's account data from the backend
  const fetchAccountData = useCallback(async () => {
    try {
      const response = await axios.get(`${baseURL}/account`, {
        withCredentials: true,
      });
      // Set the user data as the response
      setUser({
        user_id: response.data.user_id,
        firstname: response.data.firstname,
        lastname: response.data.lastname,
        email: response.data.email,
        address: response.data.address,
        balance: response.data.balance,
      });
    } catch (error) {
      // Error messaging
      if (error.response && error.response.status === 401) {
        throw new Error("Unauthorized");
      }
      console.error("Failed to fetch account data:", error);
    }
  }, []);

  // Handle updating an account field on the backend
  const handleSave = async () => {
    // Separate check for passwords match
    if (editingField === "password") {
      const { newPassword, confirmPassword } = passEdit;
      if (newPassword !== confirmPassword) {
        alert("Passwords do not match.");
        return;
      }
      try {
        await axios.patch(
          `${baseURL}/account/update/${editingField}`,
          { value: passEdit.newPassword },
          { withCredentials: true }
        );
        // Update the user
        setUser((prevUser) => ({ ...prevUser, [editingField]: editValue }));
        setEditingField(null); // exit edit mode
        setPassEdit({ newPassword: "", confirmPassword: "" });
      } catch (error) {
        // Error messaging
        console.error(`Failed to update ${editingField}:`, error);
        alert(`Failed to update ${editingField}. Please try again.`);
      }
    } else {
      try {
        await axios.patch(
          `${baseURL}/account/update/${editingField}`,
          { value: editValue },
          { withCredentials: true }
        );
        // Update the user
        setUser((prevUser) => ({ ...prevUser, [editingField]: editValue }));
        setEditingField(null); // exit edit mode
        setEditValue("");
      } catch (error) {
        if (error.response && error.response.status === 400) {
          // Show alert for the specific error
          alert("An account with this email already exists.");
      } else {
          // General error handling for other errors
          console.error(`Failed to update ${editingField}:`, error);
          alert(`Failed to update ${editingField}. Please try again.`);
      }
      }
    }
    // alert(`Updated successfully!`);
  };

  // Handle confirming a transaction
  const handleConfirmTransaction = async () => {
    const amount = parseFloat(transactionAmount);

    if (isNaN(amount) || amount <= 0) {
      alert("Invalid amount. Please enter a valid number greater than zero.");
      return;
    }

    const newBalance =
      transactionType === "withdraw"
        ? user.balance - amount
        : user.balance + amount;

    if (newBalance < 0) {
      setTransactionAmount("");
      setTransactionSource("");
      setShowTransactionInput(false);
      setShowConfirmation(false);
      alert("Insufficient funds for withdrawal. Transaction canceled.");
      return;
    }

    try {
      await axios.patch(
        `${baseURL}/account/update/balance`,
        { value: newBalance },
        { withCredentials: true }
      );
      setUser((prevUser) => ({ ...prevUser, balance: newBalance }));
      setTransactionAmount("");
      setTransactionSource("");
      setShowTransactionInput(false);
      setShowConfirmation(false);
      // alert(
      //   `Transaction successful! Your new balance is $${newBalance.toFixed(2)}.`
      // );
    } catch (error) {
      const errorMessage =
        error.response?.data?.message ||
        "Transaction failed. Please try again.";
      alert(errorMessage);
    }
  };

  // Handle transaction button click
  const handleTransactionButtonClick = (type) => {
    const action = type === "withdraw" ? "withdraw funds" : "deposit funds";
    setTransactionType(type);
    setShowTransactionInput(true);
  };

  // Handle cancel
  const handleCancel = () => {
    setEditingField(null);
    setEditValue("");
    setTransactionType("");
    setTransactionAmount("");
    setShowTransactionInput(false);
    setShowConfirmation(false);
  };

  // Set the appropriate editing field
  const handleEdit = (field) => {
    setEditingField(field);
  };

  useEffect(() => {
    fetchAccountData();
  }, [fetchAccountData]);

  return (
    <div className="profile-info">
      <ul>
        {/* User details for the logged user */}
        <li>
          <span>First Name </span>
          {/* Update the editing field, same for all fields */}
          {editingField === "firstname" ? (
            <div className="profile-edit">
              <input
                type="text"
                value={editValue}
                placeholder="Updated First Name"
                onChange={(e) => setEditValue(e.target.value)}
              />
              <div className="confirmation-buttons">
                <button className="save-button" onClick={handleSave}>
                  Save
                </button>
                <button className="cancel-button" onClick={handleCancel}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="profile-data">
              {user.firstname}
              {/* Edit button, same for all fields */}
              <img
                src={pencil}
                alt="Edit"
                className="edit-button"
                onClick={() => handleEdit("firstname")}
              />
            </div>
          )}
        </li>
        <li>
          <span>Last Name </span>
          {editingField === "lastname" ? (
            <div className="profile-edit">
              <input
                type="text"
                value={editValue}
                placeholder="Updated Last Name"
                onChange={(e) => setEditValue(e.target.value)}
              />
              <div className="confirmation-buttons">
                <button className="save-button" onClick={handleSave}>
                  Save
                </button>
                <button className="cancel-button" onClick={handleCancel}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="profile-data">
              {user.lastname}
              <img
                src={pencil}
                alt="Edit"
                className="edit-button"
                onClick={() => handleEdit("lastname")}
              />
            </div>
          )}
        </li>
        <li>
          <span>Email </span>
          {editingField === "email" ? (
            <div className="profile-edit">
              <input
                type="text"
                value={editValue}
                placeholder="New Email Address"
                onChange={(e) => setEditValue(e.target.value)}
              />
              <div className="confirmation-buttons">
                <button className="save-button" onClick={handleSave}>
                  Save
                </button>
                <button className="cancel-button" onClick={handleCancel}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="profile-data">
              {user.email}
              <img
                src={pencil}
                alt="Edit"
                className="edit-button"
                onClick={() => handleEdit("email")}
              />
            </div>
          )}
        </li>
        <li>
          <span>Address </span>
          {editingField === "address" ? (
            <div className="profile-edit">
              <input
                type="text"
                placeholder="New Address"
                value={editValue}
                onChange={(e) => setEditValue(e.target.value)}
              />
              <div className="confirmation-buttons">
                <button className="save-button" onClick={handleSave}>
                  Save
                </button>
                <button className="cancel-button" onClick={handleCancel}>
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="profile-data">
              {user.address}
              <img
                src={pencil}
                alt="Edit"
                className="edit-button"
                onClick={() => handleEdit("address")}
              />
            </div>
          )}
        </li>
        <li>
          <span>Account Balance </span> {/* Round the user balance */}
          <p className="profile-data">${user.balance?.toFixed(2)}</p>
          <div className="transaction-section">
            {!showTransactionInput && !showConfirmation && (
              <div className="transaction-buttons">
                <button
                  className="withdraw-button"
                  onClick={() => handleTransactionButtonClick("withdraw")}
                >
                  Withdraw
                </button>
                <button
                  className="deposit-button"
                  onClick={() => handleTransactionButtonClick("deposit")}
                >
                  Deposit
                </button>
              </div>
            )}

            {showTransactionInput && !showConfirmation && (
              <div className="transaction-input">
                <input
                  type="number"
                  placeholder="Enter amount"
                  value={transactionAmount}
                  onChange={(e) => setTransactionAmount(e.target.value)}
                />
                <input
                  type="text"
                  placeholder={
                    transactionType === "withdraw"
                      ? "Routing Number to Withdraw"
                      : "Routing Number to Deposit"
                  }
                  value={transactionSource}
                  onChange={(e) => setTransactionSource(e.target.value)}
                />
                <div className="confirmation-buttons">
                  <button
                    className="withdraw-button"
                    onClick={() => setShowConfirmation(true)}
                  >
                    {transactionType === "withdraw" ? "Withdraw" : "Deposit"}
                  </button>
                  <button
                    className="trans-cancel-button"
                    onClick={handleCancel}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {/* Transaction confirmation message and buttons */}
            {showConfirmation && (
              <div className="transaction-confirmation">
                <p>
                  Are you sure you want to {transactionType} $
                  {transactionAmount}?
                </p>
                <div className="confirmation-buttons">
                  <button
                    className="confirm-button"
                    onClick={handleConfirmTransaction}
                  >
                    Confirm
                  </button>
                  <button
                    className="trans-cancel-button"
                    onClick={handleCancel}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}
          </div>
        </li>

        {/* Password-specific editing */}
        {editingField === "password" ? (
          <div className="profile-edit">
            {/* Has both a password and confirm password entry */}
            <input
              className="pw-input"
              type="password"
              placeholder="New Password"
              value={passEdit.newPassword}
              onChange={(e) =>
                setPassEdit({ ...passEdit, newPassword: e.target.value })
              }
            />
            <input
              className="pw-input"
              type="password"
              placeholder="Confirm New Password"
              value={passEdit.confirmPassword}
              onChange={(e) =>
                setPassEdit({ ...passEdit, confirmPassword: e.target.value })
              }
            />
            <div className="confirmation-buttons">
              <button className="save-button" onClick={handleSave}>
                Save
              </button>
              <button className="cancel-button" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <li onClick={() => handleEdit("password")}>Edit Password</li>
        )}
      </ul>
      {/* Show the user their user ID */}
      <p className="uid">Information for User #{user.user_id}</p>
    </div>
  );
};

export default ProfileInfo;
