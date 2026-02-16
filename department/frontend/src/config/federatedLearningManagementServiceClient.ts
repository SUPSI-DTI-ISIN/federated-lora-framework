import {Configuration, ManagementApi} from "@isin/federated-learniAdapterAping-management-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    basePath: '',
    baseOptions: axiosInstance.defaults
});

export const federatedLearningManagementApi = new ManagementApi(config);