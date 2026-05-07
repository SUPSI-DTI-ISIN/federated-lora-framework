import {useMutation, useQueryClient} from "@tanstack/react-query";
import {departmentAdaptersApi} from "../../../config/mlflowServiceClient.ts";

interface DeleteDepartmentAdaptersParams {
    modelKey: string;
    adapterVersion: number;
}

export const useDeleteDepartmentAdapters = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, DeleteDepartmentAdaptersParams>({
        mutationFn: async ({modelKey, adapterVersion}: DeleteDepartmentAdaptersParams) => departmentAdaptersApi.deleteAdapterVersionApiMlflowModelModelKeyAdaptersAdapterVersionDelete(modelKey, adapterVersion).then(response => response.data),
        onSuccess: () => {
            queryClient.invalidateQueries({queryKey: ["department-adapters"]})
        }
    })
}