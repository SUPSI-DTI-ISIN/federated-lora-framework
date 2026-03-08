import {useQuery} from "@tanstack/react-query";
import type {FederatedLearningJobDTO} from "@isin/federated-learning-management-service-client";
import {federatedLearningJobsApi} from "../../../config/federatedLearningManagementServiceClient.ts";

export const useGetFederatedLearningJobById = (federatedLearningJobId: number) => {
    return useQuery<FederatedLearningJobDTO, Error>({
        queryKey: ['federated-learning-jobs', federatedLearningJobId],
        queryFn: async () => federatedLearningJobsApi.getFederatedLearningJobByIdApiFederatedLearningManagementJobsJobIdGet(federatedLearningJobId).then(response => response.data)
    })
}