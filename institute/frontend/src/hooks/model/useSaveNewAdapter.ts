import {useMutation, useQueryClient} from "@tanstack/react-query";
import {adaptersApi} from "../../config/modelServiceClient.ts";
import type {AdapterDTO, AvailableAdaptersDTO} from "@isin/model-service-client";


interface SaveNewAdapterParams {
    modelKey: string;
    adapterVersion: number;
}

export const useSaveNewAdapter = () => {
    const queryClient = useQueryClient();

    return useMutation<AdapterDTO, Error, SaveNewAdapterParams>({
        mutationFn: async ({modelKey, adapterVersion}: SaveNewAdapterParams) => adaptersApi.saveNewAdapterApiModelModelModelKeyAdaptersPost(
            modelKey,
            {
                version: adapterVersion
            }
        ).then(response => response.data),
        onSuccess: (newAdapterDTO: AdapterDTO, {modelKey}) => {
            queryClient.setQueryData(
                ["adapters"],
                (oldData: AvailableAdaptersDTO) => {
                    if (!oldData) return { model_key: modelKey, adapters: [newAdapterDTO] };

                    return {
                        ...oldData,
                        adapters: oldData.adapters ? [newAdapterDTO, ...oldData.adapters] : [newAdapterDTO],
                    };
                }
            );

            queryClient.setQueryData<AvailableAdaptersDTO>(
                ["adapters", "local"],
                (oldData) => {
                    if (!oldData) return { model_key: modelKey, adapters: [newAdapterDTO] };

                    return {
                        ...oldData,
                        adapters: oldData.adapters ? [newAdapterDTO, ...oldData.adapters] : [newAdapterDTO],
                    };
                }
            );

            queryClient.invalidateQueries({queryKey: ["adapters"]})
            queryClient.invalidateQueries({queryKey: ["adapters", "local"]})
        }
    })
}