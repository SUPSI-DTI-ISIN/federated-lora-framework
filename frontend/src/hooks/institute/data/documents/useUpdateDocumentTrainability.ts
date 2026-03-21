import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

interface UpdateDocumentTrainabilityParams {
    documentId: number;
    isTrainable: boolean;
}

export const useUpdateDocumentTrainability = () => {
    const queryClient = useQueryClient();
    const {documentsApi} = useDataApi();

    return useMutation<DocumentDTO, Error, UpdateDocumentTrainabilityParams>({
        mutationFn: async ({documentId, isTrainable}: UpdateDocumentTrainabilityParams) => documentsApi.updateDocumentTrainableApiDataDocumentsDocumentIdPut(
            documentId,
            {
                is_trainable: isTrainable
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