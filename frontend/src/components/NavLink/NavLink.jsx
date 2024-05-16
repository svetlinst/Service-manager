import {Link} from "react-router-dom";
import PropTypes from "prop-types";

const NavLink = ({path, label, action}) => {
    return (
        <li className="nav-item">
            <Link
                className="nav-link active"
                aria-current="page"
                to={path}
                onClick={action}
            >
                {label}
            </Link>
        </li>
    )
}

NavLink.propTypes = {
    path: PropTypes.string,
    label: PropTypes.string,
    action: PropTypes.func,
}

export default NavLink;