import sharedStyles from "../../assets/styles/SharedStyles.module.css";

const HEADER_TEXT = 'Service Request Details'

const ServiceRequestDetailHeader = () => {
    return (
        <header className={sharedStyles.roundedContainerPrimary}>
            {HEADER_TEXT}
        </header>
    )
}

export default ServiceRequestDetailHeader;