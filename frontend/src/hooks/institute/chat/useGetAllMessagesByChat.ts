import {useQuery} from "@tanstack/react-query";
import type {MessageDTO} from "@isin/chat-service-client";
import {useChatApi} from "../../api/useChatApi.ts";

export const useGetAllMessagesByChat = (chatId: number) => {
    const {messagesApi} = useChatApi();

    return useQuery<MessageDTO[], Error>({
        queryKey: ['messages', chatId],
        queryFn: async () => messagesApi.getMessagesApiChatChatsChatIdMessagesGet(chatId).then(response => response.data)
    })
}