// IMPORTS
import React from "react";
import { PiFlowerTulipDuotone } from "react-icons/pi";

import plantGuy from "../assets/plant_guy.png";

import "./styles/HomePage.css";

// HOME PAGE
function HomePage() {
  return (
    <div className="home-container">
      <img src={plantGuy}></img>
      <h1>Welcome to Zamazon!</h1>
      <h2>
        <PiFlowerTulipDuotone size={24} />{" "}
        Your favorite plant store <PiFlowerTulipDuotone size={24} />
      </h2>
    </div>
  );
}

export default HomePage;
