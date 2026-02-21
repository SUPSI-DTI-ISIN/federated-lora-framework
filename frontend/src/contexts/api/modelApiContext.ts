import { createContext } from "react";
import type {AdaptersApi} from "@isin/model-service-client";

interface ModelApiContextType {
    adaptersApi: AdaptersApi;
}

export const ModelApiContext = createContext<ModelApiContextType | undefined>(undefined);