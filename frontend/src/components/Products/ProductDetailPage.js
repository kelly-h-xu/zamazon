import React from "react";
import { useState, useEffect } from "react";
import axios from "axios";
import { FaLessThan } from "react-icons/fa";
import { Link, useLocation } from "react-router-dom";

import ProductListing from "./ProductListing";
import { baseURL } from "../../config";
import MyProductReview from "../Social/MyProductReview";
import ProductRatingSummary from "../Social/ProductRatingSummary";
import ProductReviews from "../Social/ProductReviews";

import "../styles/Products/ProductDetail.css";
import "../styles/Socials/MyProductReview.css"
import "../styles/Socials/Reviews.css"

function ProductDetailPage() {
  const location = useLocation();
  const { product_name } = location.state || {}; // Access passed state
  const [productListings, setProductListings] = useState([]);
  const [product, setProduct] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!product_name) return; // Ensure product_name exists before making the API call
      try {
        const listingsResponse = await axios.get(
          `${baseURL}/products_listings/${encodeURIComponent(product_name)}`
        );
        const productResponse = await axios.get(
          `${baseURL}/products/${encodeURIComponent(product_name)}`
        );
        setProductListings(listingsResponse.data);
        setProduct(productResponse.data[0]);
      } catch (err) {
        console.error("Failed to fetch listings:", err);
        setError("Failed to fetch product listings.");
      }
    };

    fetchData();
  }, [product_name]);
  console.log("product", product);
  console.log("product listings", productListings);

  if (!product_name) {
    return <p>Product data not found.</p>;
  }

  return (
    <div className="product-page-container">
      <Link to={`/products/${product.category}`} className="back-button">
        <FaLessThan className="icon" />
        <h4 className="back-text">Back</h4>
      </Link>
      <div className="product-detail-page">
        <div className="product-details">
          <div className="product-header-wrapper">
            <div className="product-info">
              <h2 className="product-name">{product_name}</h2>
              {product.total_reviews > 0 && (
                <div>
                  Average Rating:
                  {"★".repeat(Math.floor(product.avg_rating)) +
                    "☆".repeat(5 - Math.floor(product.avg_rating))}{" "}
                  {product.avg_rating} <br />({product.total_reviews} reviews)
                </div>
              )}
            </div>
            <img src={product.image_url} alt={`image of ${product_name}`} />
          </div>
          <p className="product-description">{product.description}</p>
        </div>

        {/* Listings Section */}
        <div className="seller-listings">
          <h2 style={{ color: "#8dc365" }}>Sellers</h2>
          <div className="listings-border">
            {productListings.length > 0 ? (
              productListings.map((listing) => (
                <ProductListing key={listing.product_id} listing={listing} />
              ))
            ) : (
              <p>No listings available.</p>
            )}
          </div>
        </div>
      </div>

      {/* Reviews Section at Bottom */}
      <div className="parent-reviews-container">
        <h2>Reviews</h2>
        <hr className="review-divider" />
        <div className="reviews-section-container">
          {product.total_reviews > 0 ? (
            <>
              <div className="rating-summary-container">
                <ProductRatingSummary productName={product_name} />
              </div>
              <div className="review-elements-container">
                <MyProductReview productName={product_name} />
                <ProductReviews productName={product_name} />
              </div>
            </>
          ) : (
            <h4 style={{fontWeight: "300", fontStyle: "italic", color: "#666"}}>No Reviews for this product yet</h4>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProductDetailPage;
