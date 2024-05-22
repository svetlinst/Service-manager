import {useAuth} from "../../contexts/AuthContext.jsx";
import NavLink from "../NavLink/NavLink.jsx";
import React from "react";

const NavBar = () => {
    const {logout, userDetails} = useAuth();
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            {userDetails && (<p>{userDetails.profile.last_name}</p>)}
            <div className="container-fluid">
                <a className="navbar-brand" href="/public">My App</a>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <NavLink label='Home' path={'/'}/>

                        {!userDetails && (
                            <NavLink label='Login' path='/login'/>
                        )}

                        {userDetails && (
                            <React.Fragment>
                                <NavLink label='Service Requests' path='/service_requests'/>
                                <NavLink label='User Profile' path='/profile'/>
                                <NavLink label='Logout' action={() => logout()} path='/'/>
                            </React.Fragment>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    )
}

export default NavBar;
