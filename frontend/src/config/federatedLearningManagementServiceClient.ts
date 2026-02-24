import {Configuration, JobsApi} from "@isin/federated-learning-management-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    basePath: '',
    baseOptions: axiosInstance.defaults
});

export const federatedLearningJobsApi = new JobsApi(config);