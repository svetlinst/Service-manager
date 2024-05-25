import PropTypes from "prop-types";
import {useState} from "react";
import Button from "../common/Button/Button.jsx";
import FormLabel from "../common/FormLabel/FormLabel.jsx";
import sharedStyles from '../../assets/styles/SharedStyles.module.css'
import Select from "../common/Select/Select.jsx";
import Input from "../common/Input/Input.jsx";
import TextArea from "../common/TextArea/TextArea.jsx";

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
                        <div className={sharedStyles.marginBottomMid}>
                            <FormLabel labelText={field.label} htmlFor={field.name}/>
                            <Select
                                id={field.name}
                                name={field.name}
                                value={formData[field.name] || ''}
                                onChange={handleChange}
                                options={field.options}
                            />
                        </div>
                    ) : field.type === 'textarea' ? (
                        <div>
                            <FormLabel labelText={field.label} htmlFor={field.name}/>
                            <TextArea
                                id={field.name}
                                name={field.name}
                                value={formData[field.name] || ''}
                                onChange={handleChange}
                            />
                        </div>
                    ) : (
                        <div className={sharedStyles.marginBottomMid}>
                            <FormLabel labelText={field.label} htmlFor={field.name}/>
                            <Input
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