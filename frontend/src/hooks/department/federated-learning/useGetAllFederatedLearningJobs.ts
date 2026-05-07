import {useQuery} from "@tanstack/react-query";
import type {FederatedLearningJobDTO} from "@isin/federated-learning-management-service-client";
import {federatedLearningJobsApi} from "../../../config/federatedLearningManagementServiceClient.ts";

export const useGetAllFederatedLearningJobs = () => {
    return useQuery<FederatedLearningJobDTO[], Error>({
        queryKey: ['federated-learning-jobs'],
        queryFn: async () => federatedLearningJobsApi.getAllFederatedLearningJobApiFederatedLearningManagementJobsGet().then(response => response.data)
    })
}