import type {ReactNode} from "react";
import {ApiBasePathProvider} from "./ApiBasePathProvider.tsx";
import {ChatApiProvider} from "./ChatApiProvider.tsx";
import {DataApiProvider} from "./DataApiProvider.tsx";
import {ModelApiProvider} from "./ModelApiProvider.tsx";

interface ApiProvidersProps {
    children: ReactNode;
}

export const ApiProviders = ({children}: ApiProvidersProps) => {
    return (
        <ApiBasePathProvider>
            <ChatApiProvider>
                <DataApiProvider>
                    <ModelApiProvider>
                        {children}
                    </ModelApiProvider>
                </DataApiProvider>
            </ChatApiProvider>
        </ApiBasePathProvider>
    )
}