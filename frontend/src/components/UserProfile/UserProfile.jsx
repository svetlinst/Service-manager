import {getProfileData, getCustomerDetails} from "../../services/get_data.js";
import {useState, useEffect} from "react";
import {useAuth} from "../../contexts/AuthContext.jsx";
import UserProfileDetails from "../UserProfileDetails/UserProfileDetails.jsx";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner.jsx";
import CustomerDetails from "../CustomerDetails/CustomerDetails.jsx";

const UserProfile = () => {
    const [profile, setProfile] = useState({});
    const {token, userDetails} = useAuth();
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [customerDetails, setCustomerDetails] = useState(undefined);
    // todo: consolidate loading spinner to wait for customer information
    const [isLoadingCustomer, setIsLoadingCustomer] = useState(true);

    useEffect(() => {
        if (userDetails) {
            getProfileData(userDetails.id, token).then(
                data => {
                    setProfile(data);
                    setIsLoading(false);

                    console.log(data);
                    console.log(userDetails);
                }
            ).catch(
                err => {
                    setError('Error while fetching the data!')
                    console.log(err);
                })
        }
    }, [token, userDetails]);

    useEffect(() => {
        if (userDetails) {
            setIsLoadingCustomer(true);
            getCustomerDetails(userDetails.customer_id, token).then((data) => {
                setCustomerDetails(data);
                setIsLoadingCustomer(false);
            })
        }
    }, [token, userDetails]);

    return (
        <div>
            <div>
                {
                    error ? (<p>{error}</p>) : isLoading || !userDetails ? (<LoadingSpinner/>) : (
                        <UserProfileDetails
                            last_name={profile.last_name}
                            first_name={profile.first_name}
                            phone_number={profile.phone_number}
                            email={userDetails.email}
                            id={userDetails.id}
                        />
                    )
                }
            </div>
            <div>
                {!isLoadingCustomer && (
                    <CustomerDetails
                        name={customerDetails.name}
                        vat={customerDetails.vat}
                        email={customerDetails.email_address}
                        phoneNumber={customerDetails.phone_number}
                    />
                )}
            </div>
        </div>


    )
}

export default UserProfile