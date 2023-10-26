import React from "react";
import classes from "./Card.modules.css";

function Card(props) {
    return <div className={classes.card}>{props.children}</div>;
}

export default Card;
