// IMPORTS
import React, { useState, useEffect } from "react";
import axios from "axios";

import { baseURL } from "../../config";

// PRODUCT RATING SUMMARY 
function ProductRatingSummary({productName}) {
    const [ratingSummary, setRatingSummary] = useState({});

    useEffect(() => {
        // Function grabs product rating summary from backend
        const fetchRatingSummary = async () => {
            try {
                const response = await axios.get(`${baseURL}/get_product_rating_summary/${productName}`);
                setRatingSummary(response.data);
            } catch (error) {
                console.error("Failed to fetch rating summary:", error);
            }
        };
        
    // Call function to update review summary
    fetchRatingSummary();
    }, [productName]);

    return (
        <div>
            <h3>Rating Summary</h3>
            <p>Average Rating: {parseFloat(ratingSummary.average_rating).toFixed(2) || "N/A"}</p>
            <p>Lowest Rating: {ratingSummary.lowest_rating || "N/A"}</p>
            <p>Highest Rating: {ratingSummary.highest_rating || "N/A"}</p>
            <p>Total Ratings: {ratingSummary.total_ratings || "N/A"}</p>
        </div>
    );
}

export default ProductRatingSummary;
