import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {FederatedLearningJobDTO} from "@isin/federated-learning-management-service-client";
import {federatedLearningJobsApi} from "../../../config/federatedLearningManagementServiceClient.ts";

export const useStartFederatedLearning = () => {
    const queryClient = useQueryClient();

    return useMutation<FederatedLearningJobDTO, Error>({
        mutationFn: async () => federatedLearningJobsApi.startFederatedLearningApiFederatedLearningManagementJobsPost().then(response => response.data),
        onSuccess: (newFederatedLearningJob: FederatedLearningJobDTO) => {
            queryClient.setQueryData<FederatedLearningJobDTO[]>(["federated-learning-jobs"], (oldData) => {
                return oldData ? [...oldData, newFederatedLearningJob] : [newFederatedLearningJob];
            });
        }
    })
}