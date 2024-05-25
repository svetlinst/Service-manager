import PropTypes from "prop-types";
import classes  from './Select.module.css'

const Select = ({id, name, value, onChange, options}) => {
    return (
        <select
            id={id}
            name={name}
            value={value || ''}
            onChange={onChange}
        >
            {options.map((option) => (
                <option key={option.value} value={option.value}>
                    {option.label}
                </option>
            ))}
        </select>
    )
}

Select.propTypes = {
    id: PropTypes.string,
    name: PropTypes.string,
    value: PropTypes.string,
    onChange: PropTypes.func,
    options: PropTypes.arrayOf(PropTypes.shape({
        value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
        label: PropTypes.string
    }))
}

export default Select;