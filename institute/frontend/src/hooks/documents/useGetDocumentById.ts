import {useQuery} from "@tanstack/react-query";
import {documentsApi} from "../../config/dataServiceClient.ts";
import type {DocumentDTO} from "@isin/data-service-client";

export const useGetDocumentById = (documentId: string) => {
    return useQuery<DocumentDTO, Error>({
        queryKey: ['documents', documentId],
        queryFn: async () => documentsApi.getByIdApiDataDocumentsDocumentIdGet(documentId).then(response => response.data)
    })
}