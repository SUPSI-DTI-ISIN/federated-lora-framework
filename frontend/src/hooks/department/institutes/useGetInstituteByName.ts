import {useQuery} from "@tanstack/react-query";
import type {InstituteDTO} from "@isin/institute-service-client";
import {instituteApi} from "../../../config/instituteServiceClient.ts";

export const useGetInstituteByName = (instituteName?: string) => {
    return useQuery<InstituteDTO, Error>({
        queryKey: ['institutes', "name", instituteName],
        queryFn: async () => instituteApi.getInstituteByNameApiInstituteInstitutesNameInstituteNameGet(instituteName!).then(response => response.data),
        enabled: !!instituteName
    })
}