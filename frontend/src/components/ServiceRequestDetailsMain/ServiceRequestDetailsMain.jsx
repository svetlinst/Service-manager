import Button from "../common/Button/Button.jsx";
import Form from "../common/Form/Form.jsx";
import LoadingSpinner from "../LoadingSpinner/LoadingSpinner.jsx";
import sharedStyles from '../../assets/styles/SharedStyles.module.css';
import PropTypes from "prop-types";

const STATUS_TEXT = 'Status';
const PROBLEM_DESCRIPTION_TEXT = 'Problem description';
const RESOLUTION_TEXT = 'Resolution';
const EDIT_BUTTON_TEXT = 'Edit';

const ServiceRequestDetailsMain = ({
                                       serviceRequest,
                                       allowEdit,
                                       handleEdit,
                                       fields,
                                       handleSave,
                                       handleClose,
                                       isSubmitting,
                                       submitError
                                   }) => {
    const style = `${sharedStyles.horizontalFlex} ${sharedStyles.flexJustifyStretch}`
    return (
        <main className={sharedStyles.roundedContainerSecondary}>
            <p>{STATUS_TEXT}: {serviceRequest['status_display']}</p>
            <div className={sharedStyles.horizontalFlex}>
                {allowEdit ? (
                    <p>{PROBLEM_DESCRIPTION_TEXT}: {serviceRequest['problem_description']}</p>
                ) : (
                    <div className={sharedStyles.horizontalFlex}>
                        {submitError && <p>{submitError}</p>}
                        <Form onSubmit={handleSave} fields={fields} onCancel={handleClose}
                              initialValues={{problem_description: serviceRequest.problem_description}}/>
                        {isSubmitting && <LoadingSpinner/>}
                    </div>
                )}
                {allowEdit && <Button onClick={handleEdit}>{EDIT_BUTTON_TEXT}</Button>}
            </div>
            <p>{RESOLUTION_TEXT}: {serviceRequest['resolution']}</p>
        </main>
    );
};

ServiceRequestDetailsMain.propTypes = {
    serviceRequest: PropTypes.object,
    allowEdit: PropTypes.bool,
    handleEdit: PropTypes.func,
    handleSave: PropTypes.func,
    handleClose: PropTypes.func,
    isSubmitting: PropTypes.bool,
    submitError: PropTypes.string,
    fields: PropTypes.array
}

export default ServiceRequestDetailsMain;