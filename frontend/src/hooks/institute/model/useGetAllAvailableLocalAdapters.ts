import {useQuery} from "@tanstack/react-query";
import type {AvailableAdaptersDTO} from "@isin/model-service-client";
import {useModelApi} from "../../api/useModelApi.ts";

export const useGetAllAvailableLocalAdapters = (modelKey: string) => {
    const {adaptersApi} = useModelApi();

    return useQuery<AvailableAdaptersDTO, Error>({
        queryKey: ['adapters', 'local'],
        queryFn: async () => adaptersApi.getAvailableLocalAdaptersApiModelModelsModelKeyAdaptersLocalGet(
            modelKey
        ).then(response => response.data)
    })
}