import {useQuery} from "@tanstack/react-query";
import type {AvailableAdaptersDTO} from "@isin/model-service-client";
import {useModelApi} from "../../api/useModelApi.ts";

export const useGetAllAvailableAdapters = (modelKey: string) => {
    const {adaptersApi} = useModelApi();

    return useQuery<AvailableAdaptersDTO, Error>({
        queryKey: ['adapters'],
        queryFn: async () => adaptersApi.getAvailableAdaptersApiModelModelModelKeyAdaptersGet(
            modelKey
        ).then(response => response.data)
    })
}