import {useMutation, useQueryClient} from "@tanstack/react-query";
import {documentsApi} from "../../config/dataServiceClient.ts";

export const useDeleteDocument = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, string>({
        mutationFn: async (documentId: string) => documentsApi.deleteByIdApiDataDocumentsDocumentIdDelete(documentId).then(response => response.data),
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["documents"]})
        }
    })
}