import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {ChatDTO} from "@isin/chat-service-client";
import {useChatApi} from "../../api/useChatApi.ts";

export const useDeleteChat = () => {
    const queryClient = useQueryClient();
    const {chatApi} = useChatApi();

    return useMutation<void, Error, number>({
        mutationFn: async (chatId: number) => chatApi.deleteChatApiChatChatsChatIdDelete(chatId).then(response => response.data),
        onSuccess: (_, chatId: number) => {
            queryClient.setQueryData<ChatDTO[]>(["chats"], (old) =>
                old ? old.filter((chat) => chat.id !== chatId) : old
            );
        }
    })
}