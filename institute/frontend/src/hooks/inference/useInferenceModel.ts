import {useMutation} from "@tanstack/react-query";
import type {QueryResponseDTO} from "@isin/inference-service-client";
import {inferenceApi} from "../../config/inferenceServiceClient.ts";

export interface InferenceModelParams {
    modelKey: string;
    adapterVersion: number | null;
    prompt: string;
}

export const useInferenceModel = () => {
    return useMutation<QueryResponseDTO, Error, InferenceModelParams>({
        mutationFn: async ({modelKey, adapterVersion, prompt}: InferenceModelParams) => inferenceApi.queryApiInferenceInferenceQueryPost(
            {
                model_key: modelKey,
                adapter_version: adapterVersion,
                prompt: prompt
            }
        ).then(response => response.data),
    })
}