import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import AccountPage from "./components/AccountPage";
import AddProduct from "./components/AddProduct";
import { AuthProvider } from "./components/AuthContext";
import CartPage from "./components/CartPage";
import HomePage from "./components/HomePage";
import Login from "./components/Login";
// import Inventory from './components/Inventory';
// import PurchaseHistoryPage from './components/PurchaseHistoryPage';
// import SocialPage from './components/SocialPage';
import Navbar from "./components/Navbar";
import OrderDetails from "./components/OrderDetails";
import ProductNavbar from "./components/ProductNavbar";
import ProductDetailPage from "./components/Products/ProductDetailPage";
import ProductPage from "./components/Products/ProductPage";
import Register from "./components/Register";
import UpdateProduct from "./components/UpdateProduct";
import UserDetailsPage from "./components/UserDetailsPage";
import UserSearchPage from "./components/UserSearchPage";

// import logo from './logo.svg';
import "./App.css";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <ProductNavbar />
        <div>
          {/* defining routes */}
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/account" element={<AccountPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/users" element={<UserSearchPage />} />
            <Route path="/register" element={<Register />} />
            {/* Below moved to account tabs */}
            {/* <Route path="/inventory" element={<Inventory/>} /> */}
            {/* <Route path="/purchases" element={<PurchaseHistoryPage/>} /> */}
            {/* <Route path="/socials" element={<SocialPage/>} /> */}
            <Route path="/products/:category" element={<ProductPage />} />
            <Route path="/product/:productName" element={<ProductDetailPage />} />
            <Route path="/user/:userId" element={<UserDetailsPage />} />
            <Route path="/order/:purchaseID" element={<OrderDetails />} />
          
            <Route path="/add_product" element={<AddProduct />} />
            <Route path='/update_product/' element={<UpdateProduct/>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
