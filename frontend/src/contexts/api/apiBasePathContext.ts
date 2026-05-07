import {createContext} from "react";

export type ApiBasePathContextType = {
    basePath: string;
};

export const ApiBasePathContext = createContext<ApiBasePathContextType | undefined>(undefined);