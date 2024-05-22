import {getDataDetail} from "../services/get_data.js";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner.jsx'
import {useAuth} from "../contexts/AuthContext.jsx";

const ServiceRequestDetail = () => {
    const {id} = useParams()
    const [isLoading, setIsLoading] = useState(true)
    const [serviceRequest, setServiceRequest] = useState({});
    const [error, setError] = useState(null);
    const {token} = useAuth();

    useEffect(() => {
        setIsLoading(true);
        getDataDetail(id, token).then(
            res => {
                setServiceRequest(res);
                setIsLoading(false);
            }
        ).catch(err => {
            setError('Error while fetching the data!')
            setIsLoading(false);
        })
    }, [id]);

    return (
        <div>
            {
                isLoading ? (<LoadingSpinner/>) : error ? (
                    <p>{error}</p>
                ) : (
                    <p>Detail {serviceRequest.id}</p>
                )
            }
        </div>
    )
}

export default ServiceRequestDetail;
