import React, { useEffect, useState } from "react";
import axios from "axios";
import { useParams, useSearchParams } from 'react-router-dom';

import Pagination from "@mui/material/Pagination"; // pagination component keeps track of current page as "page"
import Filter from "./Filter";
import ProductCard from "./ProductCard";
import ProductSearch from "./ProductSearch";
import { baseURL } from "../../config";

import "../styles/Products/ProductPage.css";
import "../styles/Products/ProductsPagination.css";

function ProductPage() {
 const { category } = useParams();
 const [products, setProducts] = useState([]);
 const [totalPages, setTotalPages] = useState(0);
 const [errorMessage, setErrorMessage] = useState("");
 const [currentPage, setCurrentPage] = useState(1);
 const [selectedFilter, setSelectedFilter] = useState("None");
 const [search, setSearch] = useState(""); // search term state
 const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    const initialSearch = searchParams.get("search") || "";
    setSearch(initialSearch);
  }, [searchParams]);

 function handleFilter(event) {
   setSelectedFilter(event.target.value);
 }

 const handleSearchChange = (event) => {
  const newSearch = event.target.value;
  setSearch(newSearch);  // update the search state with the new value
  setSearchParams({ search: newSearch});
};

 useEffect(() => {
   const fetchProductsData = async () => {
     try {
       const response = await axios.get(
         `${baseURL}/products?category=${category}&page=${currentPage}&filter=${selectedFilter}&search=${search}`
       );
       const { products, totalPages } = response.data;
       setProducts(products);
       setTotalPages(totalPages);
     } catch (error) {
       console.error("Error fetching data:", error);
     }
   };

   // Fetch products when category, currentPage, selectedFilter, or search term changes
   fetchProductsData();
 }, [category, currentPage, selectedFilter, search]); // include 'search' in the dependency array

 return (
   <div className="product-page">
     <div className="controls">
       <ProductSearch search={search} handleSearchChange={handleSearchChange} />
       <Filter handleFilter={handleFilter} />
     </div>
     <div className="product-list">
       {products.map((product) => (
         <ProductCard key={product.product_id} product={product} />
       ))}
     </div>
     <div className="pagination">
       <Pagination
         count={totalPages}
         shape="rounded"
         siblingCount={2}
         onChange={(event, page) => setCurrentPage(page)} // update currentPage when pagination changes
         sx={{
           "& .MuiPaginationItem-page.Mui-selected": {
             backgroundColor: "#273e14", 
             color: "white",        
           },
         }}
       />
     </div>
   </div>
 );
}
export default ProductPage;
