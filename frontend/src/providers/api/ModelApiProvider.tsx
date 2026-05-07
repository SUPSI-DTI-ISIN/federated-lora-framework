import {type ReactNode, useMemo} from "react";
import {useApiBasePath} from "../../hooks/api/useApiBasePath.ts";
import {axiosInstance} from "../../config/axios.ts";
import {ModelApiContext} from "../../contexts/api/modelApiContext.ts";
import {AdaptersApi, Configuration} from "@isin/model-service-client";

interface ModelApiProviderProps {
    children: ReactNode;
}

export const ModelApiProvider = ({ children }: ModelApiProviderProps) => {
    const { basePath } = useApiBasePath();

    const value = useMemo(() => {
        const config = new Configuration({
            basePath,
            baseOptions: axiosInstance.defaults,
        });

        return {
            adaptersApi: new AdaptersApi(config),
        };
    }, [basePath]);

    return (
        <ModelApiContext.Provider value={value}>
            {children}
        </ModelApiContext.Provider>
    );
};
