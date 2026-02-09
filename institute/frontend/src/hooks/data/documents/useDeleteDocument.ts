import {useMutation, useQueryClient} from "@tanstack/react-query";
import {documentsApi} from "../../../config/dataServiceClient.ts";
import type {DocumentDTO} from "@isin/data-service-client";

export const useDeleteDocument = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, number>({
        mutationFn: async (documentId: number) => documentsApi.deleteByIdApiDataDocumentsDocumentIdDelete(documentId).then(response => response.data),
        onSuccess: (_, documentId: number) => {
            queryClient.setQueryData<DocumentDTO[]>(["documents"], (old) =>
                old ? old.filter((document) => document.id !== documentId) : old
            );
        }
    })
}