import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {DocumentDTO, SectionDTO} from "@isin/data-service-client";
import {useDataApi} from "../../../api/useDataApi.ts";

interface UpdateSectionContentParams {
    sectionId: number;
    documentId: number;
    updatedContent: string;
}


export const useUpdateSectionContent = () => {
    const queryClient = useQueryClient();
    const {sectionsApi} = useDataApi();

    return useMutation<SectionDTO, Error, UpdateSectionContentParams>({
        mutationFn: async ({sectionId, updatedContent}: UpdateSectionContentParams) => sectionsApi.updateSectionApiDataSectionsSectionIdPut(
            sectionId,
            {
                updated_content: updatedContent
            }
        ).then(response => response.data),
        onSuccess: (updatedSectionDTO, {sectionId, documentId}: UpdateSectionContentParams) => {
            queryClient.setQueryData<DocumentDTO>(
                ["documents", documentId],
                (old) => {
                    if (!old) return old;

                    return {
                        ...old,
                        sections: old.sections.map((section) =>
                            section.id === sectionId
                                ? updatedSectionDTO
                                : section
                        ),
                    };
                }
            );
        }
    })
}