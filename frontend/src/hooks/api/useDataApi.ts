import {useContext} from "react";
import {DataApiContext} from "../../contexts/api/dataApiContext.ts";

export const useDataApi = () => {
    const context = useContext(DataApiContext);
    if (!context)
        throw new Error("useDataApi must be used within DataApiProvider");
    return context;
};