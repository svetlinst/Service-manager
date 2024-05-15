import ServiceRequestItem from "./ServiceRequestItem.jsx";
import PropTypes from "prop-types";
import Button from "./Button/Button.jsx";
import {Link} from "react-router-dom";

const ServiceRequestList = ({service_requests}) => {
    return(
        <div>
            <Link className="nav-link active" aria-current="page" to={`/service_requests/create`} ><Button>Create New</Button></Link>
            {service_requests.map((service_request) => (
                <ServiceRequestItem key={service_request.id} {...service_request}/>
            ))}
        </div>
    )
}

ServiceRequestList.propTypes = {
    service_requests: PropTypes.array,
}

export default ServiceRequestList;