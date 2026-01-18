import axios from "axios";

export const axiosInstance = axios.create();

export const setAuthToken = (token: string | null) => {
    if (token) {
        axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    } else {
        delete axiosInstance.defaults.headers.common["Authorization"];
    }
};