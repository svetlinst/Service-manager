import PropTypes from "prop-types";
import {useState} from "react";
import Button from "../Button/Button.jsx";

const Form = ({onSubmit, fields}) => {
    const [formData, setFormData] = useState({});

    const handleChange = (e) => {
        setFormData({...formData, [e.target.name]: e.target.value});
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit}>
            {fields.map((field) => (
                <div key={field.name}>
                    {field.type === 'dropdown' ? (
                        <div>
                            <label htmlFor={field.name}>{field.label}</label>
                            <select
                                id={field.name}
                                name={field.name}
                                value={formData[field.name] || ''}
                                onChange={handleChange}
                            >
                                {field.options.map((option) => (
                                    <option key={option.value} value={option.value}>
                                        {option.label}
                                    </option>
                                ))}
                            </select>
                        </div>
                    ) : (
                        <div>
                            <label htmlFor={field.name}>{field.label}</label>
                            <input
                                type={field.type}
                                id={field.name}
                                name={field.name}
                                value={formData[field.name] || ''}
                                onChange={handleChange}
                            />
                        </div>
                    )}
                </div>
            ))}
            <Button>Submit</Button>
        </form>
    )
}

Form.propTypes = {
    onSubmit: PropTypes.func,
    fields: PropTypes.array,
}


export default Form;