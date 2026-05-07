import { createContext } from "react";
import type { ChatApi, MessagesApi } from "@isin/chat-service-client";

interface ChatApiContextType {
    chatApi: ChatApi;
    messagesApi: MessagesApi;
}

export const ChatApiContext = createContext<ChatApiContextType | undefined>(undefined);