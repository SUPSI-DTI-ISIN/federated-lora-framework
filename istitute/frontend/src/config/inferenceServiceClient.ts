import {Configuration, InferenceApi} from "@isin/inference-service-client"
import {axiosInstance} from "./axios.ts";

const config = new Configuration({
    baseOptions: axiosInstance.defaults
});

export const inferenceApi = new InferenceApi(config);