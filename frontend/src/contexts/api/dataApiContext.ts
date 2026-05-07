import { createContext } from "react";
import type {DocumentsApi, SectionsApi} from "@isin/data-service-client";

interface DataApiContextType {
    documentsApi: DocumentsApi;
    sectionsApi: SectionsApi;
}

export const DataApiContext = createContext<DataApiContextType | undefined>(undefined);