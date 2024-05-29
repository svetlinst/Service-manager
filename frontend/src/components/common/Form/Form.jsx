import PropTypes from "prop-types";
import {useState} from "react";
import Button from "../Button/Button.jsx";
import FormLabel from "../FormLabel/FormLabel.jsx";
import sharedStyles from '../../../assets/styles/SharedStyles.module.css'
import Select from "../Select/Select.jsx";
import Input from "../Input/Input.jsx";
import TextArea from "../TextArea/TextArea.jsx";
import classes from './Form.module.css';

const Form = ({onSubmit, fields, onCancel, initialValues}) => {
    const [formData, setFormData] = useState(initialValues || {});

    const handleChange = (e) => {
        setFormData({...formData, [e.target.name]: e.target.value});
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    const renderField = (field, formData, handleChange, key) => {
        switch (field.type) {
            case 'dropdown':
                return (
                    <div key={key} className={sharedStyles.marginBottomMid}>
                        <FormLabel labelText={field.label} htmlFor={field.name}/>
                        <Select
                            id={field.name}
                            name={field.name}
                            value={formData[field.name] || ''}
                            onChange={handleChange}
                            options={field.options}
                        />
                    </div>
                );
            case 'textarea':
                return (
                    <div key={key}>
                        <FormLabel labelText={field.label} htmlFor={field.name}/>
                        <TextArea
                            id={field.name}
                            name={field.name}
                            value={formData[field.name] || ''}
                            onChange={handleChange}
                        />
                    </div>
                );
            default:
                return (
                    <div key={key} className={sharedStyles.marginBottomMid}>
                        <FormLabel labelText={field.label} htmlFor={field.name}/>
                        <Input
                            type={field.type}
                            id={field.name}
                            name={field.name}
                            value={formData[field.name] || ''}
                            onChange={handleChange}
                        />
                    </div>
                );
        }
    }

    return (
        <form className={classes.appForm} onSubmit={handleSubmit}>
            {fields.map((field, index) => renderField(field, formData, handleChange, field.id || index))}
            <Button>Submit</Button>
            {onCancel && <Button type='button' onClick={onCancel}>Cancel</Button>}
        </form>
    )
}

Form.propTypes = {
    onSubmit: PropTypes.func,
    fields: PropTypes.array,
    onCancel: PropTypes.func,
    initialValues: PropTypes.object,
}


export default Form;