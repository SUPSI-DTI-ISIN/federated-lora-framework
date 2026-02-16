import {useMutation, useQueryClient} from "@tanstack/react-query";
import {adaptersApi} from "../../config/mlflowServiceClient.ts";
import type {ModelAdaptersVersionDTO} from "@isin/mlflow-service-client";

interface UseDeleteAdapterParams {
    modelKey: string;
    adapterVersion: number;
}

export const useDeleteAdapter = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, UseDeleteAdapterParams>({
        mutationFn: async ({modelKey, adapterVersion}) => adaptersApi.deleteAdapterVersionApiMlflowModelModelKeyAdaptersAdapterVersionDelete(
            modelKey,
            adapterVersion
        ).then(response => response.data),
        onSuccess: (_, {adapterVersion}) => {
            queryClient.setQueryData<ModelAdaptersVersionDTO>(["adapters"], (old) => {
                if (!old?.adapters_version) return old;

                return {
                    ...old,
                    adapters_version: old.adapters_version.filter(
                        (version) => version !== adapterVersion
                    ),
                };
            });
        }
    })
}