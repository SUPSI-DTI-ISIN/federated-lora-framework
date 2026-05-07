import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

interface useUploadDocumentParams {
    file: File;
    isExternallyApproved: boolean;
}

export const useUploadDocument = () => {
    const queryClient = useQueryClient();
    const {documentsApi} = useDataApi();

    return useMutation<DocumentDTO, Error, useUploadDocumentParams>({
        mutationFn: async ({file, isExternallyApproved}: useUploadDocumentParams) => documentsApi.uploadApiDataDocumentsUploadPost(
            isExternallyApproved,
            file
        ).then(response => response.data),
        onSuccess: (uploadedDocument: DocumentDTO) => {
            queryClient.setQueryData<DocumentDTO[]>(["documents"], (old) =>
                old ? [...old, uploadedDocument] : [uploadedDocument]
            );
        }
    })
}