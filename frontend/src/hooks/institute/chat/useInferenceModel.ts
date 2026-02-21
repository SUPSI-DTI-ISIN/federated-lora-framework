import {useMutation, useQueryClient} from "@tanstack/react-query";
import type {MessageDTO} from "@isin/chat-service-client";
import {useChatApi} from "../../api/useChatApi.ts";

export interface InferenceModelParams {
    chatId: number;
    modelKey: string;
    adapterVersion: number | null;
    prompt: string;
}

export const useInferenceModel = () => {
    const queryClient = useQueryClient();
    const {messagesApi} = useChatApi();

    return useMutation<MessageDTO, Error, InferenceModelParams>({
        mutationFn: async ({chatId, modelKey, adapterVersion, prompt}: InferenceModelParams) => messagesApi.sendMessageApiChatChatChatIdMessagesPost(
            chatId,
            {
                model_key: modelKey,
                adapter_version: adapterVersion,
                prompt: prompt
            }
        ).then(response => response.data),
        onSuccess: (assistantOutputMessage, {chatId}) => {
            queryClient.setQueryData<MessageDTO[]>(["messages", chatId], (oldData) => {
                return oldData ? [...oldData, assistantOutputMessage] : [assistantOutputMessage];
            });
        }
    })
}