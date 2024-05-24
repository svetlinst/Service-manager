import ServiceRequestItem from "../ServiceRequestItem/ServiceRequestItem.jsx";
import PropTypes from "prop-types";

const ServiceRequestList = ({service_requests}) => {
    return (
        <div>
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