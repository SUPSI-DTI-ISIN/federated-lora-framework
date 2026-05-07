import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {InstituteDTO} from "@isin/institute-service-client";
import {instituteApi} from "../../../config/instituteServiceClient.ts";

interface UpdateInstituteBody {
    name?: string;
    url?: string;
}

interface UpdateInstituteParams {
    instituteId: number;
    updateInstituteBody: UpdateInstituteBody;
}

export const useUpdateInstitute = () => {
    const queryClient = useQueryClient();

    return useMutation<InstituteDTO, Error, UpdateInstituteParams>({
        mutationFn: async ({instituteId, updateInstituteBody}: UpdateInstituteParams) => instituteApi.updateInstituteApiInstituteInstitutesInstituteIdPut(
            instituteId,
            {
                name: updateInstituteBody.name,
                url: updateInstituteBody.url
            }
        ).then(response => response.data),
        onSuccess: (updatedInstitute: InstituteDTO) => {
            queryClient.setQueryData<InstituteDTO[]>(["institutes"], (oldData) => {
                if (!oldData) return [updatedInstitute];

                return oldData.map((institute) =>
                    institute.id === updatedInstitute.id ? updatedInstitute : institute
                );
            });
        }
    })
}