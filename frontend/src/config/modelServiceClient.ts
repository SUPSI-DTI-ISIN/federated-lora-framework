import {Configuration, AdaptersApi} from "@isin/model-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    basePath: '',
    baseOptions: axiosInstance.defaults
});

export const adaptersApi = new AdaptersApi(config);