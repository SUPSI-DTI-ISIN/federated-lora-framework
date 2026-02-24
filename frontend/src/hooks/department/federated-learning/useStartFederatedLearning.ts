import {useMutation} from "@tanstack/react-query";
import {federatedLearningJobsApi} from "../../../config/federatedLearningManagementServiceClient.ts";
import type {FederatedLearningJobStartResponseDTO} from "@isin/federated-learning-management-service-client";

export const useStartFederatedLearning = () => {
    //const queryClient = useQueryClient();

    return useMutation<FederatedLearningJobStartResponseDTO, Error>({
        mutationFn: async () => federatedLearningJobsApi.startFederatedLearningApiFederatedLearningManagementJobsPost().then(response => response.data),
        onSuccess: () => {
            console.log("Start federated learning")
        }
    })
}