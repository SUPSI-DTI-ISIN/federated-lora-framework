import {useMutation} from "@tanstack/react-query";
import type {QueryResponseDTO} from "@isin/inference-service-client";
import {inferenceApi} from "../../config/inferenceServiceClient.ts";

export const useInferenceModel = () => {
    return useMutation<QueryResponseDTO, Error, string>({
        mutationFn: async (prompt: string) => inferenceApi.queryApiInferenceInferenceQueryPost({prompt}).then(response => response.data),
    })
}