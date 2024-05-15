import {getData} from '../services/get_data.js'
import ServiceRequestList from "../components/ServiceRequestList.jsx";
import {useEffect, useState} from "react";
import LoadingSpinner from "../components/LoadingSpinner.jsx";

const ServiceRequests = () => {
    const [serviceRequestItems, setServiceRequestItems] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        getData().then(
            data => {
                setServiceRequestItems(data);
                setIsLoading(false);
            }
        ).catch(err => {
            setError('Error while fetching the data!')
            setIsLoading(false);
        })
    }, []);

    return (
        <div className="container">
            {
                isLoading ? <LoadingSpinner/> : error ? (
                    <p>{error}</p>
                ) : (
                    <ServiceRequestList service_requests={serviceRequestItems}/>
                )
            }
        </div>
    )
}

export default ServiceRequests;