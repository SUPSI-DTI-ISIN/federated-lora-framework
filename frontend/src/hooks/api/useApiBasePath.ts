import {useContext} from "react";
import {ApiBasePathContext} from "../../contexts/api/apiBasePathContext.ts";

export const useApiBasePath = () => {
    const context = useContext(ApiBasePathContext);
    if (!context) {
        throw new Error("useApiBasePath must be used within ApiBasePathProvider");
    }
    return context;
}