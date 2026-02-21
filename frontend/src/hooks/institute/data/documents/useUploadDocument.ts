import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

export const useUploadDocument = () => {
    const queryClient = useQueryClient();
    const {documentsApi} = useDataApi();

    return useMutation<DocumentDTO, Error, File>({
        mutationFn: async (file: File) => documentsApi.uploadApiDataDocumentsUploadPost(file).then(response => response.data),
        onSuccess: (uploadedDocument: DocumentDTO) => {
            queryClient.setQueryData<DocumentDTO[]>(["documents"], (old) =>
                old ? [...old, uploadedDocument] : [uploadedDocument]
            );
        }
    })
}