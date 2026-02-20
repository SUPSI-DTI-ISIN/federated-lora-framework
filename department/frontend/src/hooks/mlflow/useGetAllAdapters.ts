import {useQuery} from "@tanstack/react-query";
import {adaptersApi} from "../../config/mlflowServiceClient.ts";
import type {ModelAdaptersVersionDTO} from "@isin/mlflow-service-client";

export const useGetAllAdapters = (modelKey: string) => {
    return useQuery<ModelAdaptersVersionDTO, Error>({
        queryKey: ['adapters'],
        queryFn: async () => adaptersApi.getAdaptersVersionApiMlflowModelModelKeyAdaptersGet(
            modelKey
        ).then(response => response.data)
    })
}