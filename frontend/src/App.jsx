import './App.css'
import {BrowserRouter, Routes, Route} from "react-router-dom";
import Layout from "./containers/Layout.jsx";
import Home from "./containers/Home.jsx";
import ServiceRequests from "./containers/ServiceRequests.jsx";
import ServiceRequestDetail from "./containers/ServiceRequestDetail.jsx";
import ServiceRequestCreate from "./components/ServiceRequestCreate/ServiceRequestCreate.jsx";
import {AuthProvider} from "./contexts/AuthContext.jsx";
import Login from "./containers/Login.jsx";

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Layout>
                    <Routes>
                        <Route path="/" element={<Home/>}/>
                        <Route path="/service_requests" element={<ServiceRequests/>}/>
                        <Route path="/service_requests/:id" element={<ServiceRequestDetail/>}/>
                        <Route path="/service_requests/create" element={<ServiceRequestCreate/>}/>
                        <Route path="/login" element={<Login/>}/>
                    </Routes>
                </Layout>
            </BrowserRouter>
        </AuthProvider>
    )
}

export default App