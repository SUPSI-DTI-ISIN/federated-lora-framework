import {Configuration, DocumentsApi} from "@isin/data-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    basePath: '',
    baseOptions: axiosInstance.defaults
});

export const documentsApi = new DocumentsApi(config);