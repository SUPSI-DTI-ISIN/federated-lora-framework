import {type ReactNode, useMemo} from "react";
import {useApiBasePath} from "../../hooks/api/useApiBasePath.ts";
import {ChatApi, Configuration, MessagesApi} from "@isin/chat-service-client";
import {axiosInstance} from "../../config/axios.ts";
import { ChatApiContext } from "../../contexts/api/chatApiContext.ts";

interface ChatApiProviderProps {
    children: ReactNode;
}

export const ChatApiProvider = ({ children }: ChatApiProviderProps) => {
    const { basePath } = useApiBasePath();

    const value = useMemo(() => {
        const config = new Configuration({
            basePath,
            baseOptions: axiosInstance.defaults,
        });

        return {
            chatApi: new ChatApi(config),
            messagesApi: new MessagesApi(config),
        };
    }, [basePath]);

    return (
        <ChatApiContext.Provider value={value}>
            {children}
        </ChatApiContext.Provider>
    );
};
