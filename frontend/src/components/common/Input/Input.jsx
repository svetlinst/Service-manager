import PropTypes from "prop-types";
import classes from './Input.module.css'

const Input = ({type, id, name, value, onChange}) => {
    return (
        <input
            type={type}
            id={id}
            name={name}
            value={value || ''}
            onChange={onChange}
        />
    )
}

Input.propTypes = {
    type: PropTypes.string,
    id: PropTypes.string,
    name: PropTypes.string,
    value: PropTypes.string,
    onChange: PropTypes.func,
}

export default Input;