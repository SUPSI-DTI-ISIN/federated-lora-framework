import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {AdapterDTO, AvailableAdaptersDTO} from "@isin/model-service-client";
import {useModelApi} from "../../api/useModelApi.ts";


interface SaveNewAdapterParams {
    modelKey: string;
    adapterVersion: number;
}

export const useSaveNewAdapter = () => {
    const queryClient = useQueryClient();
    const {adaptersApi} = useModelApi();

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
                    ? old.adapters.map(adapter =>
                        adapter.version === newAdapter.version ? newAdapter : adapter
                    )
                    : [newAdapter],
            });

            queryClient.setQueryData<AvailableAdaptersDTO>(
                ["adapters"],
                updater
            );

            queryClient.invalidateQueries({queryKey: ["adapters", "local"]});
        }
    })
}