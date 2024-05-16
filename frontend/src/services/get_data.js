import axios from "axios";

const baseUrl = import.meta.env.VITE_APP_API_URL

export const getData = async (token) => {
    try {
        const res = await axios.get(`${baseUrl}service_requests`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
};

export const getDataDetail = async (id) => {
    try {
        const res = await axios.get(`${baseUrl}service_requests/${id}`);
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
};

export const getAllCustomers = async () => {
    const res = await axios.get(`${baseUrl}customers/names`);
    return res.data;
}

export const createServiceRequest = async (data) => {
    try {
        const res = await axios.post(`${baseUrl}service_requests/`, data);
        return res.data;
    } catch (err) {
        return Promise.reject(err);
    }
}

