import NavBar from "../components/NavBar/NavBar.jsx";
import PropTypes from "prop-types";
const Layout = ({children}) => {
    return (
        <div>
            <NavBar/>
             {children}
        </div>
    )
};

Layout.propTypes = {
    children: PropTypes.node,
};

export default Layout;