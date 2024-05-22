import {getProfileData} from "../../services/get_data.js";
import {useState, useEffect} from "react";
import {useAuth} from "../../contexts/AuthContext.jsx";

const UserProfile = () => {
    const [profile, setProfile] = useState({});
    const {token} = useAuth();

    useEffect(() => {
        try {
            const id = 2;
            getProfileData(id, token).then(
                data => {
                    setProfile(data)
                }
            )

        } catch (err) {
            console.log(err);
        }
    }, [token]);

    return (
        <div>
            {profile.first_name}
        </div>
    )
}

export default UserProfile