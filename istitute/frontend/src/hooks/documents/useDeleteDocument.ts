import {useMutation, useQueryClient} from "@tanstack/react-query";
import {documentsApi} from "../../config/dataServiceClient.ts";

export const useDeleteDocument = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, string>({
        mutationFn: async (document_id: string) => documentsApi.deleteByIdApiDataDocumentsDocumentIdDelete(document_id).then(response => response.data),
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["documents"]})
        }
    })
}