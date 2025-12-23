import {Configuration, DocumentsApi} from "@isin/data-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    baseOptions: axiosInstance.defaults
});

export const documentsApi = new DocumentsApi(config);