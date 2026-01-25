import {useMutation, useQueryClient} from "@tanstack/react-query";
import {adaptersApi} from "../../config/modelServiceClient.ts";
import type {AdapterDTO} from "@isin/model-service-client";


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
        onSuccess: (_newAdapterDTO: AdapterDTO) => {
            queryClient.invalidateQueries({queryKey: ["adapters"]})
            queryClient.invalidateQueries({queryKey: ["adapters", "local"]})
        }
    })
}