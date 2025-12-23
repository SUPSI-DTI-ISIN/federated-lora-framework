import {useQuery} from "@tanstack/react-query";
import {documentsApi} from "../../config/dataServiceClient.ts";
import type {DocumentDTO} from "@isin/data-service-client";

export const useGetAllDocuments = () => {
    return useQuery<DocumentDTO[], Error>({
        queryKey: ['documents'],
        queryFn: async () => documentsApi.getAllApiDataDocumentsGet().then(response => response.data)
    })
}