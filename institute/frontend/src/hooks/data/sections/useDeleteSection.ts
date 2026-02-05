import {useMutation, useQueryClient} from "@tanstack/react-query";
import {sectionsApi} from "../../../config/dataServiceClient.ts";
import type {DocumentDTO} from "@isin/data-service-client";

interface UseDeleteSectionParams {
    sectionId: number;
    documentId: number;
}


export const useDeleteSection = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, UseDeleteSectionParams>({
        mutationFn: async ({sectionId}: UseDeleteSectionParams) => sectionsApi.deleteSectionByIdApiDataSectionsSectionIdDelete(sectionId).then(response => response.data),
        onSuccess: (_, {sectionId, documentId}: UseDeleteSectionParams) => {
            console.log(queryClient.getQueryData(['documents', documentId]))
            queryClient.setQueryData(
                ['documents', documentId],
                (oldData: DocumentDTO) => {
                    if (!oldData) return oldData;

                    return {
                        ...oldData,
                        sections: oldData.sections.filter(
                            (section) => section.id !== sectionId
                        ),
                    };
                }
            );
            console.log(queryClient.getQueryData(['documents', documentId]))
            queryClient.invalidateQueries({queryKey: ['documents', documentId]})
        }
    })
}