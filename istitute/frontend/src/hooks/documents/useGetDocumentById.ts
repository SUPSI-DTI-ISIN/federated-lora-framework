import {useQuery} from "@tanstack/react-query";
import {documentsApi} from "../../config/dataServiceClient.ts";
import type {DocumentDTO} from "@isin/data-service-client";

export const useGetDocumentById = (document_id: string) => {
    return useQuery<DocumentDTO, Error>({
        queryKey: ['documents', document_id],
        queryFn: async () => documentsApi.getByIdApiDataDocumentsDocumentIdGet(document_id).then(response => response.data)
    })
}