import {getProfileData} from "../../services/get_data.js";
import {useState, useEffect} from "react";
import {useAuth} from "../../contexts/AuthContext.jsx";
import UserProfileDetails from "../UserProfileDetails/UserProfileDetails.jsx";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner.jsx";

const UserProfile = () => {
    const [profile, setProfile] = useState({});
    const {token, userDetails} = useAuth();
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

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

    return (
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

    )
}

export default UserProfile