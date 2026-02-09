import {Configuration, DocumentsApi, SectionsApi} from "@isin/data-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    basePath: '',
    baseOptions: axiosInstance.defaults
});

export const documentsApi = new DocumentsApi(config);
export const sectionsApi = new SectionsApi(config);