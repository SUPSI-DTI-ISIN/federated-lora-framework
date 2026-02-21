import {useQuery} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

export const useGetDocumentById = (documentId: number) => {
    const {documentsApi} = useDataApi();

    return useQuery<DocumentDTO, Error>({
        queryKey: ['documents', documentId],
        queryFn: async () => documentsApi.getByIdApiDataDocumentsDocumentIdGet(documentId).then(response => response.data)
    })
}