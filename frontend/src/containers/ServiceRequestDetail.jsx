import {getDataDetail} from "../services/get_data.js";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner.jsx'
import {useAuth} from "../contexts/AuthContext.jsx";
import ServiceRequest from "../components/ServiceRequest/ServiceRequest.jsx";

const ServiceRequestDetail = () => {
    const {id} = useParams()

    return (
        <div>
            {
                <ServiceRequest id={id} />
            }
        </div>
    )
}

export default ServiceRequestDetail;
