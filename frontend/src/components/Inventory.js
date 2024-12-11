// IMPORTS
import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import Popup from "reactjs-popup";

import Pagination from "@mui/material/Pagination";
import ProtectedPage from "./ProtectedPage";
import pencil from "../assets/edit_pencil.png";
import { baseURL } from "../config";

import "./styles/Account/Inventory.css";
import "./styles/Account/InventoryPagination.css";
import "reactjs-popup/dist/index.css";

// INVENTORY Component (Account Page)
function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const navigate = useNavigate();
  // Set items per page
  const itemsPerPage = 2;
  const [totalItems, setTotalItems] = useState(0);

  // Get Inventory Data from 8080
  const fetchInventoryData = useCallback(async () => {
    try {
      const response = await axios.get(
        `${baseURL}/my_inventory?currentPage=${currentPage}&itemsPerPage=${itemsPerPage}`,
        {
          withCredentials: true,
        }
      );
      setInventory(response.data.products);
      setTotalItems(response.data.total_items);
      console.log("Inventory:", response.data.products);
      console.log("Total Items:", response.data.total_items);
    } catch (error) {
      console.error("Error fetching inventory data:", error);
    }
  }, [itemsPerPage, currentPage]);

  useEffect(() => {
    fetchInventoryData();
  }, [fetchInventoryData]);

  // Pagination
  // TODO: Move to backend
  const totalPages = Math.ceil(totalItems / itemsPerPage);

  // Initialize quantity and price
  const [quantity, setQuantity] = useState(0);
  const [product_id, setProductId] = useState(0);
  const [price, setPrice] = useState(0);

  // Set quantity and price for each product
  const setQuantityVals = (pid, q) => {
    setProductId(pid);
    setQuantity(q);
  };

  const setPriceVals = (pid, p) => {
    setProductId(pid);
    setPrice(p);
  };

  // Handle product quantity change on 8080 backend
  const handleQuantityChange = async (event) => {
    event.preventDefault();
    await fetch(`${baseURL}/increase_stock`, {
      method: "POST",
      credentials: "include", // ensures cookies are sent
      body: JSON.stringify({ product_id: product_id, quantity: quantity }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    // Re-get the inventory data
    fetchInventoryData();
  };

  // Handle product price change on 8080 backend
  const handlePriceChange = async (event) => {
    event.preventDefault();
    await fetch(`${baseURL}/change_price`, {
      method: "POST",
      credentials: "include", // Ensures cookies are sent
      body: JSON.stringify({ product_id: product_id, price: price }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    // Re-get the inventory data
    fetchInventoryData();
  };

  // Handle listing removal on 8080 backend
  const removeListing = async (event) => {
    event.preventDefault();
    await fetch(`${baseURL}/remove_listing`, {
      method: "POST",
      credentials: "include", // Ensures cookies are sent
      body: JSON.stringify({ product_id: product_id }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    // Re-get the inventory data
    fetchInventoryData();
  };

  // On click "Update Product," navigate to /update_product
  const updateProduct = (pname, descript, img, cat) => {
    navigate("/update_product", {
      state: {
        product_name: pname,
        description: descript,
        image_url: img,
        category: cat,
      },
    });
  };

  return (
    // Ensure the user is logged in
    <ProtectedPage>
      <div className="inventory-container">
        {/* Check if the seller has items in their inventory */}
        {totalItems === 0 ? (
          <div>
            <p>No products in inventory.</p>
            <div className="inventory-button-container">
              <Link to="/add_product">
                <button className="inventory-container-button add-product">
                  Add Product
                </button>
              </Link>
            </div>
          </div>
        ) : (
          // If they do, display the items in their inventory

          <div className="display">
            <div className="inventory-button-container">
              <Link to="/add_product">
                <button className="inventory-container-button add-product">
                  Add Product
                </button>
              </Link>
            </div>
            <ul className="product-list">
              {inventory.map((product) => (
                // For each product, display its information
                <li key={product.id} className="product-card">
                  <div className="product-details">
                    {product.image_url ? (
                      <img
                        src={product.image_url}
                        alt={product.description}
                        className="product-image"
                      />
                    ) : (
                      <div className="product-image no-image">No image</div>
                    )}
                    <div className="product-info">
                      <p>Product ID: {product.id}</p>
                      <Link
                        to={`/product/${encodeURIComponent(product.name)}`}
                        state={{ product_name: product.name }}
                      >
                        <p>Product Name: {product.name}</p>
                      </Link>
                      <p>Price: ${product.price}</p>
                      {/* Allow seller to change the price */}
                      <div className="field-edit-wrapper">
                        Quantity: {product.quantity}
                        <Popup
                          onOpen={() =>
                            setQuantityVals(product.id, product.quantity)
                          }
                          trigger={<img className="edit-pencil" src={pencil} />}
                        >
                          <form method="post" onSubmit={handleQuantityChange}>
                            <label>
                              Enter a new quantity:
                              <input
                                type="number"
                                id="quantity"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                              ></input>
                              <button
                                className="inventory-container-button"
                                type="submit"
                              >
                                Update Stock
                              </button>
                            </label>
                          </form>
                        </Popup>
                      </div>
                      {/* Allow seller to change the quantity */}
                      <div className="field-edit-wrapper">
                        Category: {product.category}
                        <Popup
                          onOpen={() => setPriceVals(product.id, product.price)}
                          trigger={<img className="edit-pencil" src={pencil} />}
                        >
                          <form method="post" onSubmit={handlePriceChange}>
                            <label>
                              Enter a new price:
                              <input
                                id="price"
                                value={price}
                                type="number"
                                min="0"
                                step=".01"
                                onChange={(e) => setPrice(e.target.value)}
                              ></input>
                              <button
                                className="inventory-container-button"
                                type="submit"
                              >
                                Update Price
                              </button>
                            </label>
                          </form>
                        </Popup>
                      </div>
                      <p>{product.description}</p>
                      {/* Inform seller if they cannot modify the listing */}
                      {!product.is_creator && (
                        <p>
                          This item was created by another seller. <br />
                          Add your own product in the catalog to edit.
                        </p>
                      )}
                    </div>
                  </div>
                  {/* Allow creator to edit and all sellers to remove their listings */}
                  <div className="inventory-button-container">
                    <div>
                      {product.is_creator && (
                        <button
                          className="inventory-container-button"
                          onClick={() =>
                            updateProduct(
                              product.name,
                              product.description,
                              product.image_url,
                              product.category
                            )
                          }
                        >
                          Update Product
                        </button>
                      )}{" "}
                    </div>
                    <form method="post" onSubmit={removeListing}>
                      <button
                        className="inventory-container-button remove"
                        type="submit"
                        onClick={() => setProductId(product.id)}
                      >
                        Remove Listing
                      </button>
                    </form>
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

export default Inventory;
