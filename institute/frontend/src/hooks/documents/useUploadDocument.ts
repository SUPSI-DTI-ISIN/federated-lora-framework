import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {documentsApi} from "../../config/dataServiceClient.ts";

export const useUploadDocument = () => {
    const queryClient = useQueryClient();

    return useMutation<DocumentDTO, Error, File>({
        mutationFn: async (file: File) => documentsApi.uploadApiDataDocumentsUploadPost(file).then(response => response.data),
        onSuccess: (_uploadedDocument: DocumentDTO) => {
            queryClient.invalidateQueries({queryKey: ["documents"]})
        }
    })
}