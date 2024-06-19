import {createContext, useState, useEffect, useContext} from 'react';
import axios from 'axios';

const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({children}) => {
    const [token, setToken] = useState(localStorage.getItem('token'));
    const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));
    const [userEmail, setUserEmail] = useState(localStorage.getItem('userEmail'));
    const [userDetails, setUserDetails] = useState(null);

    const login = async (email, password) => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/bg/api/token/', {
                email,
                password,
            });
            const {access, refresh} = response.data;

            localStorage.setItem('token', access);
            localStorage.setItem('refreshToken', refresh);
            localStorage.setItem('userEmail', email);

            setUserEmail(email);
            setToken(access);
            setRefreshToken(refresh);
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    };

    //todo: move this function to the services API
    const getUserDetails = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/bg/api/users/${userEmail}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            setUserDetails(response.data);
            localStorage.setItem('userDetails', JSON.stringify(response.data));
        } catch (error) {
            console.error('Getting user details failed:', error);
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userDetails');
        setUserEmail(null);
        setToken(null);
        setRefreshToken(null);
        setUserDetails(null);
    };

    const refreshAccessToken = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/bg/api/token/refresh/', {
                refresh: refreshToken,
            });
            const {access} = response.data;
            localStorage.setItem('token', access);
            setToken(access);
        } catch (error) {
            console.error('Failed to refresh access token:', error);
            logout();
        }
    };

    useEffect(() => {
        const intervalId = setInterval(() => {
            if (token && refreshToken) {
                refreshAccessToken();
            }
        }, 600000); // Refresh the token every 10 minutes
        return () => clearInterval(intervalId);
    }, [token, refreshToken]);

    useEffect(() => {
        if (token && userEmail) {
            getUserDetails();
        }
    }, [token, userEmail]);

    return (
        <AuthContext.Provider value={{token, refreshToken, login, logout, userEmail, userDetails}}>
            {children}
        </AuthContext.Provider>
    );
};