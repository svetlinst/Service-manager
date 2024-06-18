import PropTypes from "prop-types";
import sharedStyles from '../../assets/styles/SharedStyles.module.css'
import Button from "../common/Button/Button.jsx";
import {useState} from "react";
import Form from "../common/Form/Form.jsx";
import {updateProfile} from '../../services/get_data.js'
import {useAuth} from "../../contexts/AuthContext.jsx";

const FIRST_NAME_TEXT = 'First name';
const LAST_NAME_TEXT = 'Last name';
const PHONE_NUMBER_TEXT = 'Phone number';
const EMAIL_TEXT = 'Email';

const UserProfileDetails = ({first_name, last_name, phone_number, email, id}) => {
    const styles = `${sharedStyles.horizontalFlex} ${sharedStyles.flexCentered}`;
    const [isEditTriggered, setIsEditTriggered] = useState(false);
    const {token} = useAuth();
    const [userDetails, setUserDetails] = useState({first_name, last_name, phone_number})

    const handleEdit = () => {
        setIsEditTriggered(true);
    }

    const handleSubmit = async (values) => {
        setUserDetails(values);
        try {
            console.log(values);
            const response = await updateProfile(id, token, values);
            console.log(response);
            setIsEditTriggered(false);
        } catch (err) {
            console.log(err);
        }
    }

    const handleCancel = () => {
        setIsEditTriggered(false);
    }

    const fields = [
        {name: 'first_name', label: FIRST_NAME_TEXT, type: 'input'},
        {name: 'last_name', label: LAST_NAME_TEXT, type: 'input'},
        {name: 'phone_number', label: PHONE_NUMBER_TEXT, type: 'input'},
    ]

    return (
        <div>
            <header className={sharedStyles.roundedContainerPrimary}>
                Header
            </header>
            <main className={sharedStyles.roundedContainerSecondary}>
                <section className={styles}>
                    {isEditTriggered ? (
                        <div className={sharedStyles.verticalFlex}>
                            <Form
                                fields={fields}
                                onSubmit={handleSubmit}
                                onCancel={handleCancel}
                                initialValues={userDetails}
                            />
                            <p>{EMAIL_TEXT}: {email}</p>
                        </div>

                    ) : (
                        <div className={sharedStyles.verticalFlex}>
                            <p>{FIRST_NAME_TEXT}: {userDetails.first_name}</p>
                            <p>{LAST_NAME_TEXT}: {userDetails.last_name}</p>
                            <p>{PHONE_NUMBER_TEXT}: {userDetails.phone_number}</p>
                            <p>{EMAIL_TEXT}: {email}</p>
                        </div>
                    )}

                    <div>
                        {!isEditTriggered && <Button onClick={handleEdit}>Edit</Button>}
                    </div>
                </section>
            </main>
        </div>
    )
}

UserProfileDetails.propTypes = {
    first_name: PropTypes.string.isRequired,
    last_name: PropTypes.string.isRequired,
    phone_number: PropTypes.string,
    email: PropTypes.string,
    id: PropTypes.number,
}

export default UserProfileDetails;