import classes from './Card.module.css'
import PropTypes from "prop-types";
import {Link} from "react-router-dom";
import Button from "../Button/Button.jsx";


const Card = ({id, customer, problem_description, resolution}) => {


    return (
        <div className={classes.card}>
            <header className={classes.cardHeader}>
                <p>Customer: {customer.name}</p>
            </header>
            <main className={classes.cardMain}>
                <p>Problem description: {problem_description}</p>
                <p>Resolution: {resolution}</p>
            </main>
            <footer className={classes.cardFooter}>
                <Link className="nav-link active" aria-current="page" to={`/service_requests/${id}`}>
                    <Button>Detail</Button>
                </Link>
            </footer>
        </div>
    );
}

Card.propTypes = {
    customer: PropTypes.object,
    problem_description: PropTypes.string,
    resolution: PropTypes.string,
    id: PropTypes.number,
}

export default Card;