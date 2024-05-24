import PropTypes from "prop-types";
import classes from './Button.module.css'

const Button = ({onClick, disabled, type, children}) => {
    return(
        <button onClick={onClick} disabled={disabled} type={type} className={classes.mainButton}>
            {children}
        </button>
    )
}

Button.propTypes = {
    onClick: PropTypes.func,
    disabled: PropTypes.bool,
    type: PropTypes.oneOf(['button', 'submit', 'reset']),
    children: PropTypes.node.isRequired,
}

Button.defaultTypes = {
    type: 'button',
}

export default Button;