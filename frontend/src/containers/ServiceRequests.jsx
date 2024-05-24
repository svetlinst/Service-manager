import { getData } from '../services/get_data.js'
import ServiceRequestList from "../components/ServiceRequestList/ServiceRequestList.jsx";
import { useEffect, useState, useRef } from "react";
import LoadingSpinner from "../components/LoadingSpinner/LoadingSpinner.jsx";
import { useAuth } from "../contexts/AuthContext.jsx";
import sharedStyles from "../assets/styles/SharedStyles.module.css";
import SearchInput from "../components/common/SearchInput/SerachInput.jsx";
import { Link } from "react-router-dom";
import Button from "../components/common/Button/Button.jsx";

const ServiceRequests = () => {
    const [serviceRequestItems, setServiceRequestItems] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const searchTextRef = useRef(searchTerm);
    const [triggerUpdate, setTriggerUpdate] = useState(false);
    const { token } = useAuth();

    const handleInputChange = (e) => {
        searchTextRef.current = e.target.value;
        setTriggerUpdate(prev => !prev);
    };

    useEffect(() => {
        const timeoutId = setTimeout(() => setSearchTerm(searchTextRef.current), 500);
        return () => clearTimeout(timeoutId);
    }, [triggerUpdate]);

    useEffect(() => {
        setIsLoading(true);
        getData(token, searchTerm)
            .then(data => {
                setServiceRequestItems(data);
                setIsLoading(false);
            })
            .catch(err => {
                setError('Error while fetching the data!');
                setIsLoading(false);
            });
    }, [token, searchTerm]);

    return (
        <div className="container">
            <header className={sharedStyles.roundedContainerPrimary}>
                <h3>Service Requests</h3>
                <section className={sharedStyles.horizontalFlex}>
                    <SearchInput placeholderText="Search..."
                                 onInputChange={handleInputChange}
                                 searchValue={searchTextRef.current}/>
                    <Link className="nav-link active" aria-current="page"
                          to={`/service_requests/create`}><Button>Create New</Button></Link>
                </section>
            </header>
            {
                isLoading ? <LoadingSpinner/> : error ? (
                    <p>{error}</p>
                ) : (
                    <main>
                        <ServiceRequestList service_requests={serviceRequestItems}/>
                    </main>
                )
            }
        </div>
    );
};

export default ServiceRequests;