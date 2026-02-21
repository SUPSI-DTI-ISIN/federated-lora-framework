import {useMutation, useQueryClient} from "@tanstack/react-query";
import {instituteApi} from "../../config/instituteServiceClient.ts";
import type {InstituteDTO} from "@isin/institute-service-client";

export const useDeleteInstitute = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, number>({
        mutationFn: async (instituteId: number) => instituteApi.deleteInstituteApiInstituteInstitutesInstituteIdDelete(instituteId).then(response => response.data),
        onSuccess: (_, instituteId: number) => {
            queryClient.setQueryData<InstituteDTO[]>(["institutes"], (old) =>
                old ? old.filter((institute) => institute.id !== instituteId) : old
            );
        }
    })
}