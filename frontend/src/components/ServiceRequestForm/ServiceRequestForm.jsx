import Form from "../Form/Form.jsx";
import {createServiceRequest, getAllCustomers} from "../../services/get_data.js";
import React, {useState, useEffect} from "react";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner.jsx";
import {useNavigate} from 'react-router-dom'
import {useAuth} from "../../contexts/AuthContext.jsx";

const ServiceRequestForm = () => {
    const [allCustomers, setAllCustomers] = useState([]);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [submitError, setSubmitError] = useState(null);
    const navigate = useNavigate();
    const {token, userDetails} = useAuth();

    console.log(userDetails);

    useEffect(() => {
        getAllCustomers(token).then(
            (data) => {
                setAllCustomers(data);
                setIsLoading(false);
            }
        ).catch(err => {
            setError('Error while fetching the data!');
            setIsLoading(false);
        })
    }, []);

    const handleSubmit = async (formData) => {
        const data = {
            'customer': Number(formData['customer']),
            'requestor_name': formData['requestor_name'],
            'requestor_phone_number': formData['requestor_phone_number'],
            'order_type': Number(formData['order_type']),
            'problem_description': formData['problem_description'],
            'resolution': null,
            'accepted_by': userDetails.profile.app_user,
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            const res = await createServiceRequest(data, token);
            navigate('/service_requests');
            console.log(res);
        } catch (err) {
            setSubmitError('Error wile submitting the request!');
            console.log(err);
        } finally {
            setIsSubmitting(false);
        }
    }

    const fields = [
        {
            name: 'customer', label: 'Customer', type: 'dropdown', options:
                [
                    {'value': '', 'label': ''},
                    ...allCustomers.map((customer) => ({'value': customer.id, 'label': customer.name}))
                ]
        },
        {name: 'requestor_name', label: 'Requestor name', type: 'text'},
        {name: 'requestor_phone_number', label: 'Phone number', type: 'text'},
        {
            name: 'order_type', label: 'Request type', type: 'dropdown', options: [
                {label: '', value: ''},
                {label: 'Service', value: '1'},
                {label: 'Delivery', value: '2'},
            ]
        },
        {name: 'problem_description', label: 'Problem description', type: 'text'},
    ];

    return (
        <div>
            {
                isLoading ? <LoadingSpinner/> : error ? (
                    <p>{error}</p>
                ) : (
                    <React.Fragment>
                        {submitError && <p>{submitError}</p>}
                        <Form onSubmit={handleSubmit} fields={fields}/>
                        {isSubmitting && <LoadingSpinner/>}
                    </React.Fragment>
                )
            }
        </div>
    )
}

export default ServiceRequestForm;