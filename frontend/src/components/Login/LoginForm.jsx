import {useAuth} from "../../contexts/AuthContext.jsx";
import {useState} from "react";
import {useNavigate} from "react-router-dom";

const LoginForm = () => {
    const {login} = useAuth();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            await login(email, password);
            navigate('/');
        } catch (error) {
            // Handle login error
            console.error('Login failed:', error);
        }
    };

    return (
        <div>
            <input
                type="text"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>
        </div>
    );
}

export default LoginForm;