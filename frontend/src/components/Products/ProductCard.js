import React from "react";
import { Link } from "react-router-dom";

import "../styles/Products/ProductCard.css";

function ProductCard({ product }) {
  const {
    product_id,
    product_name,
    seller_id,
    min_price,
    quantity,
    category,
    image_url,
    description,
    creator_id,
    avg_rating,
    total_reviews,
    total_purchases,
  } = product;

  return (
    <div className="product-card">
      <div className="product-header-wrapper">
        <img src={image_url} alt={product_name} className="product-image" />
        <div className="product-info">
          {/* TODO: make this link to a page for the product in the catalog */}
          <Link
            to={`/product/${encodeURIComponent(product_name)}`}
            state={{ product_name: product_name }}
          >
            <h2 className="product-name">{product_name}</h2>
          </Link>
          <h3 className="product-price">from ${min_price}</h3>
        </div>
      </div>
      <p className="product-description">
        {description} <br />
        {total_reviews > 0 && (
          <div>
            Average Rating:{"★".repeat(avg_rating) + "☆".repeat(Math.ceil(5-avg_rating))}{" "}
            {avg_rating} ({total_reviews} reviews) <br />
          </div>
        )}
        Total Purchases: {total_purchases}
      </p>
    </div>
  );
}

export default ProductCard;
