import React from 'react';
import "../styles/Products/ProductPage.css"; 

function Filter({handleFilter}) {
    return(
        <div className="filter-component-container">
            {/* <label>Filter By</label> */}
            <select name="filter" id="filter" onChange={handleFilter}>
            <option value = "None"> No Filter </option>
            <option value="price_low_high">Price: Low to High</option>
            <option value="price_high_low">Price: High to Low</option>
            <option value="avg_rating">Highest Average Rating</option>
            <option value="total_purchases">Highest Total Purchases</option>
            </select>

        </div>
    );
};

export default Filter;