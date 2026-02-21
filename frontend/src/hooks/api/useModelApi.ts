import {useContext} from "react";
import {ModelApiContext} from "../../contexts/api/modelApiContext.ts";

export const useModelApi = () => {
    const context = useContext(ModelApiContext);
    if (!context)
        throw new Error("useModelApi must be used within ModelApiProvider");
    return context;
};