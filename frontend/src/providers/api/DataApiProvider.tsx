import {type ReactNode, useMemo} from "react";
import {useApiBasePath} from "../../hooks/api/useApiBasePath.ts";
import {axiosInstance} from "../../config/axios.ts";
import {DataApiContext} from "../../contexts/api/dataApiContext.ts";
import {DocumentsApi, SectionsApi, Configuration} from "@isin/data-service-client";

interface DataApiProviderProps {
    children: ReactNode;
}

export const DataApiProvider = ({ children }: DataApiProviderProps) => {
    const { basePath } = useApiBasePath();

    const value = useMemo(() => {
        const config = new Configuration({
            basePath,
            baseOptions: axiosInstance.defaults,
        });

        return {
            documentsApi: new DocumentsApi(config),
            sectionsApi: new SectionsApi(config),
        };
    }, [basePath]);

    return (
        <DataApiContext.Provider value={value}>
            {children}
        </DataApiContext.Provider>
    );
};
