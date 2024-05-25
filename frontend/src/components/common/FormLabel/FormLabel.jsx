import PropTypes from "prop-types";
import classes from './FormLabel.module.css'

const FormLabel = ({labelText, htmlFor}) => {
    return (
        <label htmlFor={htmlFor}>{labelText}</label>
    )
}

FormLabel.propTypes = {
    labelText: PropTypes.string.isRequired,
    htmlFor: PropTypes.string.isRequired,
}

export default FormLabel;