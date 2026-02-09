import {useQuery} from "@tanstack/react-query";
import type {MessageDTO} from "@isin/chat-service-client";
import {messagesApi} from "../../config/chatServiceClient.ts";

export const useGetAllMessagesByChat = (chatId: number) => {
    return useQuery<MessageDTO[], Error>({
        queryKey: ['messages', chatId],
        queryFn: async () => messagesApi.getMessagesApiChatChatChatIdMessagesGet(chatId).then(response => response.data)
    })
}