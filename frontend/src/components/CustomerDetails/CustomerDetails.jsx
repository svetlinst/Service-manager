import PropTypes from "prop-types";
import {ToastContainer} from "react-toastify";
import sharedStyles from '../../assets/styles/SharedStyles.module.css';

const HEADER_TEXT = 'Customer';
const NAME_TEXT = 'Name';
const VAT_TEXT = 'VAT';
const EMAIL_TEXT = 'Email';
const PHONE_NUMBER_TEXT = 'Phone number';

const CustomerDetails = ({name, vat, email, phoneNumber}) => {
    return(
        <div>
            <header className={sharedStyles.roundedContainerPrimary}>
                {HEADER_TEXT}
            </header>
            <main className={sharedStyles.roundedContainerSecondary}>
                <section>
                    {/*{isEditTriggered ? (*/}
                    {/*    <div className={sharedStyles.verticalFlex}>*/}
                    {/*        <Form*/}
                    {/*            fields={fields}*/}
                    {/*            onSubmit={handleSubmit}*/}
                    {/*            onCancel={handleCancel}*/}
                    {/*            initialValues={profileDetails}*/}
                    {/*        />*/}
                    {/*        <p>{EMAIL_TEXT}: {email}</p>*/}
                    {/*    </div>*/}

                    {/*) : (*/}
                    {/*    <div className={sharedStyles.verticalFlex}>*/}
                    {/*        <p>{FIRST_NAME_TEXT}: {profileDetails.first_name}</p>*/}
                    {/*        <p>{LAST_NAME_TEXT}: {profileDetails.last_name}</p>*/}
                    {/*        <p>{PHONE_NUMBER_TEXT}: {profileDetails.phone_number}</p>*/}
                    {/*        <p>{EMAIL_TEXT}: {email}</p>*/}
                    {/*    </div>*/}
                    {/*)}*/}

                    <div className={sharedStyles.verticalFlex}>
                        <p>{NAME_TEXT}: {name}</p>
                        <p>{VAT_TEXT}: {vat}</p>
                        <p>{EMAIL_TEXT}: {email}</p>
                        <p>{PHONE_NUMBER_TEXT}: {phoneNumber}</p>
                    </div>

                    <div>
                        {/*{!isEditTriggered && <Button onClick={handleEdit}>Edit</Button>}*/}
                    </div>
                </section>
                <ToastContainer/>
            </main>
        </div>
    )
}

CustomerDetails.propTypes = {
    name: PropTypes.string,
    vat: PropTypes.string,
    email: PropTypes.string,
    phoneNumber: PropTypes.string,
}

export default CustomerDetails;