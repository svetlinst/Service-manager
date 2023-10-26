import React from "react";
import Card from "./ui/Card";
import classes from "./Dashboard.modules.css";

function Dashboard(props) {
    return (
        <div className={classes.container}>
            <Card>
                <header className={classes.header}>Card title</header>
            </Card>
            <Card>
                <header className={classes.header}>Card title</header>
            </Card>
            <Card>
                <header className={classes.header}>Card title</header>
            </Card>
        </div>
    );
}

export default Dashboard;
