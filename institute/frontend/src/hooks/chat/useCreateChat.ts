import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {ChatDTO} from "@isin/chat-service-client";
import {chatApi} from "../../config/chatServiceClient.ts";

interface CreationChatParams {
    title?: string | null;
}

export const useCreateChat = () => {
    const queryClient = useQueryClient();

    return useMutation<ChatDTO, Error, CreationChatParams>({
        mutationFn: async ({title}: CreationChatParams) => chatApi.createChatApiChatChatsPost(
            {
                title
            }
        ).then(response => response.data),
        onSuccess: (newChat: ChatDTO) => {
            queryClient.setQueryData<ChatDTO[]>(["chats"], (oldData) => {
                return oldData ? [...oldData, newChat] : [newChat];
            });
        }
    })
}