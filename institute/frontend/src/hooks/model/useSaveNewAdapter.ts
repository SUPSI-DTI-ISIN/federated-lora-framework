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
        onSuccess: (newAdapter: AdapterDTO, {modelKey}) => {
            const updater = (old: AvailableAdaptersDTO | undefined): AvailableAdaptersDTO => ({
                model_key: modelKey,
                adapters: old?.adapters
                    ? [newAdapter, ...old.adapters]
                    : [newAdapter],
            });

            queryClient.setQueryData<AvailableAdaptersDTO>(
                ["adapters"],
                updater
            );

            queryClient.setQueryData<AvailableAdaptersDTO>(
                ["adapters", "local"],
                updater
            );
        }
    })
}