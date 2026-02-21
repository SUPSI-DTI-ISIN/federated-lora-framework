import {useQuery} from "@tanstack/react-query";
import {departmentAdaptersApi} from "../../../config/mlflowServiceClient.ts";
import type {ModelAdaptersVersionDTO} from "@isin/mlflow-service-client";

export const useGetAllDepartmentAdapters = (modelKey: string) => {
    return useQuery<ModelAdaptersVersionDTO, Error>({
        queryKey: ['department', 'adapters'],
        queryFn: async () => departmentAdaptersApi.getAdaptersVersionApiMlflowModelModelKeyAdaptersGet(modelKey).then(response => response.data)
    })
}
