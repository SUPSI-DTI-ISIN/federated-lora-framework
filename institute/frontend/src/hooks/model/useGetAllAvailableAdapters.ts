import {useQuery} from "@tanstack/react-query";
import {adaptersApi} from "../../config/modelServiceClient.ts";
import type {AvailableAdaptersDTO} from "@isin/model-service-client";

export const useGetAllAvailableAdapters = (modelKey: string) => {
    return useQuery<AvailableAdaptersDTO, Error>({
        queryKey: ['adapters'],
        queryFn: async () => adaptersApi.getAvailableAdaptersApiModelModelModelKeyAdaptersGet(
            modelKey
        ).then(response => response.data)
    })
}