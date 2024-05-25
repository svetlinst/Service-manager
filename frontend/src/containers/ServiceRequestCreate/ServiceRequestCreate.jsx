import ServiceRequestForm from "../../components/ServiceRequestForm/ServiceRequestForm.jsx";
import sharedStyles from '../../assets/styles/SharedStyles.module.css'

// Extract header and instruction as constants
const HEADER_TEXT = "Create new Service Request";
const FORM_INSTRUCTION_TEXT = "To create a new Service Request, please fill-in the form below.";

const ServiceRequestCreate = () => {
    const formContainerClassName = `${sharedStyles.horizontalFlex} ${sharedStyles.flexJustifyCenter}`;

    return (
        <div>
            <header className={sharedStyles.roundedContainerPrimary}>
                {HEADER_TEXT}
            </header>
            <main className={sharedStyles.roundedContainerSecondary}>
                <section>
                    <p>{FORM_INSTRUCTION_TEXT}</p>
                </section>
                <section className={formContainerClassName}>
                    <ServiceRequestForm/>
                </section>
            </main>
        </div>
    )
}

export default ServiceRequestCreate;