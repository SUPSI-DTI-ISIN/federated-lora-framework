import {Configuration, AdapterApi} from "@isin/mlflow-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    basePath: '',
    baseOptions: axiosInstance.defaults
});

export const adaptersApi = new AdapterApi(config);