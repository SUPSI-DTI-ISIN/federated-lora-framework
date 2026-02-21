import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

export const useDeleteDocument = () => {
    const queryClient = useQueryClient();
    const {documentsApi} = useDataApi();

    return useMutation<void, Error, number>({
        mutationFn: async (documentId: number) => documentsApi.deleteByIdApiDataDocumentsDocumentIdDelete(documentId).then(response => response.data),
        onSuccess: (_, documentId: number) => {
            queryClient.setQueryData<DocumentDTO[]>(["documents"], (old) =>
                old ? old.filter((document) => document.id !== documentId) : old
            );
        }
    })
}