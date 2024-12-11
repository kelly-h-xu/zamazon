import React from 'react';
import "../styles/Products/ProductPage.css";

function ProductSearch({ search, handleSearchChange }) {
    return (
        <div className="product-search">
            <form className="search-form">
                <input
                    id="search-input"
                    className="search-input"
                    type="text"
                    placeholder="Type to search..."
                    value={search}
                    onChange={handleSearchChange}
                />
            </form>
        </div>
    );
}

export default ProductSearch;
