import {useEffect, useState} from "react";
import {useAuth} from "../../contexts/AuthContext.jsx";
import {getDataDetail, updateProblemDescription} from "../../services/get_data.js";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner.jsx";
import PropTypes from "prop-types";
import classes from './ServiceRequestDetail.module.css'
import ServiceRequestDetailHeader from "../ServiceRequestDetailHeader/ServiceRequestDetailHeader.jsx";
import ServiceRequestDetailsFooter from "../ServiceRequestDetailsFooter/ServiceRequestDetailsFooter.jsx";
import ServiceRequestDetailsMain from "../ServiceRequestDetailsMain/ServiceRequestDetailsMain.jsx";


const ServiceRequest = ({id}) => {
    const [serviceRequest, setServiceRequest] = useState({});
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const {token} = useAuth();
    const [allowEdit, setAllowEdit] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState(null);

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

    const handleEdit = () => {
        setAllowEdit(false);
    }

    const handleSave = async (formData) => {
        const data = {
            problem_description: formData.problem_description,
        }
        setIsSubmitting(true);
        setSubmitError(null);

        try {
            const res = await updateProblemDescription(serviceRequest.id, data, token);
            setServiceRequest(prevState => (
                {
                    ...prevState,
                    updated_on: res.updated_on,
                    problem_description: data.problem_description
                }
            ))
        } catch (err) {
            setSubmitError(err);
            console.log(err)
        } finally {
            setAllowEdit(true);
            setIsSubmitting(false);
        }
    }

    const handleClose = () => {
        setAllowEdit(true);
    }

    const fields = [
        {
            name: 'problem_description',
            label: 'Problem description',
            type: 'textarea',
        },
    ]

    return (
        <div className='container'>
            {isLoading ? (
                <LoadingSpinner/>
            ) : error ? (
                <p>{error}</p>
            ) : (
                <div>
                    <ServiceRequestDetailHeader/>
                    <ServiceRequestDetailsMain
                        serviceRequest={serviceRequest}
                        allowEdit={allowEdit}
                        handleEdit={handleEdit}
                        fields={fields}
                        handleSave={handleSave}
                        handleClose={handleClose}
                        isSubmitting={isSubmitting}
                        submitError={submitError}
                    />
                    <ServiceRequestDetailsFooter serviceRequest={serviceRequest}/>
                </div>
            )}
        </div>
    )
}

ServiceRequest.propTypes = {
    id: PropTypes.string,
}

export default ServiceRequest;