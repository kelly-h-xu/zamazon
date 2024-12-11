// IMPORTS
import React, { useState, useCallback, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import Pagination from "@mui/material/Pagination";
import ProductReviewForm from "./ProductReviewForm";
import SellerReviewForm from "./SellerReviewForm";
import { baseURL } from "../../config";
import ProtectedPage from "../ProtectedPage";

import "../styles/Socials/SocialCenter.css";
import "../styles/Socials/SocialPagination.css";

// SOCIAL CENTER Component (Account Page)
function SocialCenter() {
  const [productReviews, setProductReviews] = useState([]);
  const [sellerReviews, setSellerReviews] = useState([]);
  const [currentProductPage, setCurrentProductPage] = useState(1);
  const [currentSellerPage, setCurrentSellerPage] = useState(1);
  const [productTotalPages, setProductTotalPages] = useState(1);
  const [sellerTotalPages, setSellerTotalPages] = useState(1);
  const itemsPerPage = 2;

  // Track the review being edited (for both product and seller)
  const [editingProductReviewId, setEditingProductReviewId] = useState(null);
  const [editingSellerReviewId, setEditingSellerReviewId] = useState(null);

  // Fetch reviews from the backendd
  const fetchReviews = useCallback(async () => {
    try {
      const response = await axios.get(
        `${baseURL}/my_reviews?productPage=${currentProductPage}&itemsPerProductPage=${itemsPerPage}&sellerPage=${currentSellerPage}&itemsPerSellerPage=${itemsPerPage}`,
        { withCredentials: true }
      );

      // Update state with paginated data
      setProductReviews(response.data.product_reviews || []);
      setSellerReviews(response.data.seller_reviews || []);
      setProductTotalPages(response.data.product_total_pages || 1);
      setSellerTotalPages(response.data.seller_total_pages || 1);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        throw new Error("Unauthorized");
      }
      console.error("Failed to fetch reviews:", error);
    }
  }, [currentProductPage, currentSellerPage, itemsPerPage]);

  // Fetch reviews to display from backend
  useEffect(() => {
    fetchReviews();
  }, [fetchReviews]);

  // Helper function to convert rating to stars
  const renderStars = (rating) => {
    return "★".repeat(rating) + "☆".repeat(5 - rating);
  };

  // Handle review form submission (write/edit) for both product and seller
  const handleReviewFormSubmit = () => {
    setEditingProductReviewId(null); // Exit product editing mode
    setEditingSellerReviewId(null); // Exit seller editing mode
    fetchReviews(); // Refresh reviews after update
  };

  const handleReviewFormCancel = () => {
    setEditingProductReviewId(null); // Cancel product editing mode
    setEditingSellerReviewId(null); // Cancel seller editing mode
  };

  // Handle deletion of product reviews
  const handleDeleteProductReview = async (productName) => {
    if (!window.confirm("Are you sure you want to delete this product review?"))
      return;
    try {
      const response = await axios.delete(
        `${baseURL}/delete_product_review/${productName}`,
        {
          withCredentials: true,
        }
      );
      console.log(response.data.status);
      await fetchReviews(); // Refresh reviews after deletion

      // If the current page becomes empty, navigate to the previous page
      if (productReviews.length === 1 && currentProductPage > 1) {
        setCurrentProductPage((prevPage) => prevPage - 1);
      }
    } catch (error) {
      console.error("Error deleting product review:", error);
      console.log("Failed to delete product review");
    }
  };

  // Handle deletion of seller reviews
  const handleDeleteSellerReview = async (sellerId) => {
    if (!window.confirm("Are you sure you want to delete this seller review?"))
      return;

    try {
      const response = await axios.delete(
        `${baseURL}/delete_seller_review/${sellerId}`,
        {
          withCredentials: true,
        }
      );
      console.log(response.data.status);
      await fetchReviews(); // refresh reviews after deletion
      // If the current page becomes empty, navigate to the previous page
      if (sellerReviews.length === 1 && currentSellerPage > 1) {
        setCurrentSellerPage((prevPage) => prevPage - 1);
      }
    } catch (error) {
      console.error("Error deleting seller review:", error);
      console.log("Failed to delete seller review");
    }
  };

  return (
    <ProtectedPage>
      <div className="social-container">
        {/* PRODUCT REVIEWS */}
        <div className="product-reviews">
          <h2>My Product Reviews</h2>
          {productReviews.length === 0 ? (
            <p className="empty">No product reviews available.</p>
          ) : (
            <>
              <ul>
                {productReviews.map((item) => (
                  <li key={item.product_name} className="review-item">
                    {/* Switch between editing and non-editing form */}
                    {editingProductReviewId === item.product_name ? (
                      <ProductReviewForm
                        formType="update"
                        review={{ rating: item.rating, comment: item.comment }}
                        productName={item.product_name}
                        buyerId={item.buyer_id}
                        onSubmit={handleReviewFormSubmit} // submit callback
                        onCancel={handleReviewFormCancel} // cancel callback
                      />
                    ) : (
                      <>
                        <strong className="product-name">
                          Product:
                          <Link
                            to={`/product/${encodeURIComponent(
                              item.product_name
                            )}`}
                            state={{ product_name: item.product_name }}
                          >
                            {item.product_name}
                          </Link>
                        </strong>
                        <div className="stars">{renderStars(item.rating)}</div>
                        <div className="comment">{item.comment}</div>
                        <div className="review-action-container">
                          <button
                            onClick={() =>
                              setEditingProductReviewId(item.product_name)
                            }
                          >
                            Edit
                          </button>
                          <button
                            onClick={() =>
                              handleDeleteProductReview(
                                item.product_name,
                                item.buyer_id
                              )
                            }
                          >
                            Delete
                          </button>
                        </div>
                      </>
                    )}
                  </li>
                ))}
              </ul>
              <div className="pagination">
                <Pagination
                  count={productTotalPages}
                  page={currentProductPage}
                  onChange={(event, page) => setCurrentProductPage(page)}
                  shape="rounded"
                  color="primary"
                />
              </div>
            </>
          )}
        </div>

        {/* SELLER REVIEWS */}
        <div className="seller-reviews">
          <h2>My Seller Reviews</h2>
          {sellerReviews.length === 0 ? (
            <p className="empty">No seller reviews available.</p>
          ) : (
            <>
              <ul>
                {sellerReviews.map((item) => (
                  <li key={item.seller_id} className="review-item">
                    {/* Switch between editing and non-editing form */}
                    {editingSellerReviewId === item.seller_id ? (
                      <SellerReviewForm
                        formType="update"
                        review={{ rating: item.rating, comment: item.comment }}
                        sellerId={item.seller_id}
                        buyerId={item.buyer_id}
                        onSubmit={handleReviewFormSubmit} // submit callback
                        onCancel={handleReviewFormCancel} // cancel callback
                      />
                    ) : (
                      <>
                        <strong className="seller-name">
                          Seller:
                          <Link to={`/user/${item.seller_id}`}>
                            {" "}
                            {item.seller_firstname} {item.seller_lastname}
                          </Link>
                        </strong>
                        <strong>Seller ID: {item.seller_id}</strong>
                        <div className="stars">{renderStars(item.rating)}</div>
                        <div className="comment">{item.comment}</div>
                        <div className="review-action-container">
                          <button
                            onClick={() =>
                              setEditingSellerReviewId(item.seller_id)
                            }
                          >
                            Edit
                          </button>
                          <button
                            onClick={() =>
                              handleDeleteSellerReview(item.seller_id)
                            }
                          >
                            Delete
                          </button>
                        </div>
                      </>
                    )}
                  </li>
                ))}
              </ul>
              <div className="pagination">
                <Pagination
                  count={sellerTotalPages}
                  page={currentSellerPage}
                  onChange={(event, page) => setCurrentSellerPage(page)}
                  shape="rounded"
                  color="primary"
                />
              </div>
            </>
          )}
        </div>
      </div>
    </ProtectedPage>
  );
}

export default SocialCenter;
