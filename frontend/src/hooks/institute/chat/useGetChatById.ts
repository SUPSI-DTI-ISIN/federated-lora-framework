import {useQuery} from "@tanstack/react-query";
import type {ChatDTO} from "@isin/chat-service-client";
import {useChatApi} from "../../api/useChatApi.ts";

export const useGetChatById = (chatId: number) => {
    const {chatApi} = useChatApi();

    return useQuery<ChatDTO, Error>({
        queryKey: ['chats', chatId],
        queryFn: async () => chatApi.getChatByIdApiChatChatsChatIdGet(chatId).then(response => response.data)
    })
}