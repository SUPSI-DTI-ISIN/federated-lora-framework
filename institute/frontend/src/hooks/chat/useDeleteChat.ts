import {useMutation, useQueryClient} from "@tanstack/react-query";
import {chatApi} from "../../config/chatServiceClient.ts";
import type {ChatDTO} from "@isin/chat-service-client";

export const useDeleteChat = () => {
    const queryClient = useQueryClient();

    return useMutation<void, Error, number>({
        mutationFn: async (chatId: number) => chatApi.deleteChatApiChatChatsChatIdDelete(chatId).then(response => response.data),
        onSuccess: (_, chatId: number) => {
            queryClient.setQueryData<ChatDTO[]>(["chats"], (old) =>
                old ? old.filter((chat) => chat.id !== chatId) : old
            );
        }
    })
}