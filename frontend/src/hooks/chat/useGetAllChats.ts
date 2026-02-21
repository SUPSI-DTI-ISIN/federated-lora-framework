import {useQuery} from "@tanstack/react-query";
import type {ChatDTO} from "@isin/chat-service-client";
import {chatApi} from "../../config/chatServiceClient.ts";

export const useGetAllChats = () => {
    return useQuery<ChatDTO[], Error>({
        queryKey: ['chats'],
        queryFn: async () => chatApi.listChatsApiChatChatsGet().then(response => response.data)
    })
}