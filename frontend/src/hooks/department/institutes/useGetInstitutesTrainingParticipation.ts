import {useQuery} from "@tanstack/react-query";
import type {InstituteTrainingParticipationDTO} from "@isin/institute-service-client";
import {instituteApi} from "../../../config/instituteServiceClient.ts";

export const useGetInstitutesTrainingParticipation = () => {
    return useQuery<InstituteTrainingParticipationDTO[], Error>({
        queryKey: ['institutes-participation'],
        queryFn: async () => instituteApi.getInstitutesTrainingParticipationApiInstituteInstitutesTrainingParticipationGet().then(response => response.data)
    })
}