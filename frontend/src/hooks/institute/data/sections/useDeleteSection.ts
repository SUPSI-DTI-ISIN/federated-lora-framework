import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

interface UseDeleteSectionParams {
    sectionId: number;
    documentId: number;
}


export const useDeleteSection = () => {
    const queryClient = useQueryClient();
    const {sectionsApi} = useDataApi();

    return useMutation<void, Error, UseDeleteSectionParams>({
        mutationFn: async ({sectionId}: UseDeleteSectionParams) => sectionsApi.deleteSectionByIdApiDataSectionsSectionIdDelete(sectionId).then(response => response.data),
        onSuccess: (_, {sectionId, documentId}: UseDeleteSectionParams) => {
            queryClient.setQueryData<DocumentDTO>(
                ["documents", documentId],
                (old) => {
                    if (!old) return old;

                    return {
                        ...old,
                        sections: old.sections.filter(
                            (section) => section.id !== sectionId
                        ),
                    };
                }
            );
        }
    })
}