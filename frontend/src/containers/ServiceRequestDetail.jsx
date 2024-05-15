import {getDataDetail} from "../services/get_data.js";
import {useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import LoadingSpinner from '../components/LoadingSpinner.jsx'

const ServiceRequestDetail = () => {
    const {id} = useParams()
    const [isLoading, setIsLoading] = useState(true)
    const [serviceRequest, setServiceRequest] = useState({});
    const [error, setError] = useState(null);

    useEffect(() => {
        setIsLoading(true);
        getDataDetail(id).then(
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
