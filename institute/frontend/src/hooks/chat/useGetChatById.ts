import {useQuery} from "@tanstack/react-query";
import type {ChatDTO} from "@isin/chat-service-client";
import {chatApi} from "../../config/chatServiceClient.ts";

export const useGetChatById = (chatId: number) => {
    return useQuery<ChatDTO, Error>({
        queryKey: ['chats', chatId],
        queryFn: async () => chatApi.getChatByIdApiChatChatsChatIdGet(chatId).then(response => response.data)
    })
}