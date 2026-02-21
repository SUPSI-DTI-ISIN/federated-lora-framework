import {useQuery} from "@tanstack/react-query";
import {adaptersApi} from "../../config/modelServiceClient.ts";
import type {AvailableAdaptersDTO} from "@isin/model-service-client";

export const useGetAllAvailableLocalAdapters = (modelKey: string) => {
    return useQuery<AvailableAdaptersDTO, Error>({
        queryKey: ['adapters', 'local'],
        queryFn: async () => adaptersApi.getAvailableLocalAdaptersApiModelModelModelKeyAdaptersLocalGet(
            modelKey
        ).then(response => response.data)
    })
}