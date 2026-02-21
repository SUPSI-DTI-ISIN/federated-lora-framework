import {useQuery} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

export const useGetAllDocuments = () => {
    const {documentsApi} = useDataApi();

    return useQuery<DocumentDTO[], Error>({
        queryKey: ['documents'],
        queryFn: async () => documentsApi.getAllApiDataDocumentsGet().then(response => response.data)
    })
}