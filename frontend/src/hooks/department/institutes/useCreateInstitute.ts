import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {InstituteDTO} from "@isin/institute-service-client";
import {instituteApi} from "../../../config/instituteServiceClient.ts";

interface CreationInstituteParams {
    name: string;
    url: string;
}

export const useCreateInstitute = () => {
    const queryClient = useQueryClient();

    return useMutation<InstituteDTO, Error, CreationInstituteParams>({
        mutationFn: async ({name, url}: CreationInstituteParams) => instituteApi.createInstituteApiInstituteInstitutesPost(
            {
                name,
                url
            }
        ).then(response => response.data),
        onSuccess: (newInstitute: InstituteDTO) => {
            queryClient.setQueryData<InstituteDTO[]>(["institutes"], (oldData) => {
                return oldData ? [...oldData, newInstitute] : [newInstitute];
            });
        }
    })
}