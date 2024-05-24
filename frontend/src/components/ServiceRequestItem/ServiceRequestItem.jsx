import PropTypes from "prop-types";
import Card from "../common/Card/Card.jsx";
import classes from './ServiceRequestItem.module.css'

const ServiceRequestItem = ({id, customer, problem_description, resolution}) => {
    return (
        <li>
            <Card id={id} customer={customer} problem_description={problem_description} resolution={resolution}/>
        </li>
    )
}

ServiceRequestItem.propTypes = {
    customer: PropTypes.object,
    problem_description: PropTypes.string,
    resolution: PropTypes.string,
    id: PropTypes.number,
}

export default ServiceRequestItem;