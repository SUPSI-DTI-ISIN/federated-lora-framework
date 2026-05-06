import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

interface useUpdateDocumentExternalApprovedParams {
    documentId: number;
    isExternallyApproved: boolean;
}

export const useUpdateDocumentExternalApproved = () => {
    const queryClient = useQueryClient();
    const {documentsApi} = useDataApi();

    return useMutation<DocumentDTO, Error, useUpdateDocumentExternalApprovedParams>({
        mutationFn: async ({documentId, isExternallyApproved}: useUpdateDocumentExternalApprovedParams) => documentsApi.updateDocumentExternallyApprovedApiDataDocumentsExternallyApprovedDocumentIdPut(
            documentId,
            {
                is_externally_approved: isExternallyApproved
            }
        ).then(response => response.data),
        onSuccess: (updatedDocument: DocumentDTO) => {
            queryClient.setQueryData<DocumentDTO[]>(["documents"], (old) => {
                if (!old) return [updatedDocument];

                return old.map((doc) =>
                    doc.id === updatedDocument.id ? updatedDocument : doc
                );
            });
        }
    })
}