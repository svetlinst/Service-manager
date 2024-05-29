import PropTypes from "prop-types";
import classes from './TextArea.module.css'

const TextArea = ({id, name, value, onChange}) => {
    return (
        <textarea
            className={classes.textArea}
            name={name}
            id={id}
            value={value}
            onChange={onChange}
            // cols="30"
            rows="5"
        />
    )
}

TextArea.propTypes = {
    id: PropTypes.string,
    name: PropTypes.string,
    value: PropTypes.string,
    onChange: PropTypes.func,
}

export default TextArea;