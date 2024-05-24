import {useEffect, useState} from "react";
import {useAuth} from "../../contexts/AuthContext.jsx";
import {getDataDetail} from "../../services/get_data.js";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner.jsx";
import PropTypes from "prop-types";
import classes from './ServiceRequest.module.css'
import sharedStyles from '../../assets/styles/SharedStyles.module.css'
import {parseISO, format} from 'date-fns';

const ServiceRequest = ({id}) => {
    const [serviceRequest, setServiceRequest] = useState({});
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const {token} = useAuth();

    useEffect(() => {
        getDataDetail(id, token).then(
            res => {
                setServiceRequest(res);
                setIsLoading(false);
                console.log(res);
            }
        ).catch(err => {
            setError('Error while fetching the data!');
            setIsLoading(false);
        })
    }, [id, token]);

    return (
        <div className='container'>
            {
                isLoading ? (<LoadingSpinner/>) : error ? (
                    <p>{error}</p>
                ) : (
                    <div>
                        <header className={sharedStyles.roundedContainerPrimary}>
                            Service Request Details
                        </header>
                        <main className={sharedStyles.roundedContainerSecondary}>
                            <p>Problem description: {serviceRequest['problem_description']}</p>
                            <p>Resolution: {serviceRequest['resolution']}</p>
                        </main>
                        <footer className={sharedStyles.roundedContainerSecondary}>
                            <div className={sharedStyles.horizontalFlex}>
                                <p>Created by: {serviceRequest['requestor_name']}</p>
                                <p>Created on: {format(parseISO(serviceRequest['created_on']), 'dd/MM/yyyy HH:mm')}</p>
                                <p>Updated on: {format(parseISO(serviceRequest['updated_on']), 'dd/MM/yyyy HH:mm')}</p>
                            </div>
                            <div className={sharedStyles.horizontalFlex}>
                                <p>Status: {serviceRequest['status_display']}</p>
                            </div>
                        </footer>

                    </div>


                )
            }
        </div>
    )
}

ServiceRequest.propTypes = {
    id: PropTypes.string,
}

export default ServiceRequest;