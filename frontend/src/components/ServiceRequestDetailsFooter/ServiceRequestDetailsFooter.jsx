import sharedStyles from "../../assets/styles/SharedStyles.module.css";
import {format, parseISO} from "date-fns";
import PropTypes from "prop-types";

const CREATED_BY_TEXT = 'Created by'
const CREATED_ON_TEXT = 'Created on'
const UPDATED_ON_TEXT = 'Updated on'

const ServiceRequestDetailsFooter = ({serviceRequest}) => {
    return (
        <footer className={sharedStyles.roundedContainerSecondary}>
            <div className={sharedStyles.horizontalFlex}>
                <p>{CREATED_BY_TEXT}: {serviceRequest['requestor_name']}</p>
                <p>{CREATED_ON_TEXT}: {format(parseISO(serviceRequest['created_on']), 'dd/MM/yyyy HH:mm')}</p>
                <p>{UPDATED_ON_TEXT}: {format(parseISO(serviceRequest['updated_on']), 'dd/MM/yyyy HH:mm')}</p>
            </div>
        </footer>
    );
}

ServiceRequestDetailsFooter.propTypes = {
    serviceRequest: PropTypes.object,
}

export default ServiceRequestDetailsFooter;