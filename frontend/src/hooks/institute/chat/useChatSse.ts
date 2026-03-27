import { useEffect } from "react";
import {useQueryClient} from "@tanstack/react-query";
import {getChatSseUrl} from "../../../utils/sse/sseUrls.ts";
import {useAuthWrapper} from "../../auth/useAuthWrapper.ts";
import type {ChatDTO, MessageDTO} from "@isin/chat-service-client";
import {useApiBasePath} from "../../api/useApiBasePath.ts";

export const useChatSse = () => {
    const queryClient = useQueryClient();
    const {user} = useAuthWrapper();
    const { basePath } = useApiBasePath();

    useEffect(() => {
        if (!user?.profile?.sub) return;

        const eventSource = new EventSource(getChatSseUrl(basePath, user.profile.sub));

        eventSource.addEventListener("inference_job_success", async (event) => {
            try {
                const assistantMessage: MessageDTO = JSON.parse(event.data);

                queryClient.setQueryData<MessageDTO[]>(
                    ['messages', assistantMessage.chat_id],
                    (old) => old ? [...old, assistantMessage] : [assistantMessage]
                );
                queryClient.setQueryData<ChatDTO[]>(
                    ['chats'],
                    (old) => old
                        ? old.map((chat) =>
                            chat.id === assistantMessage.chat_id
                                ? {...chat, is_doing_inference: false}
                                : chat
                        )
                        : old
                );
            } catch (err) {
                console.error("Invalid SSE payload", err);
            }
        });

        eventSource.addEventListener("inference_job_failure", async (event) => {
            try {
                const parsed = JSON.parse(event.data);

                await queryClient.invalidateQueries({queryKey: ['chats']});
                await queryClient.invalidateQueries({
                    queryKey: ['messages', parsed.result.chat_id],
                    refetchType: "all"
                });
            } catch (err) {
                console.error("Invalid SSE payload", err);
            }
        })

        eventSource.onerror = (error) => {
            console.error('SSE connection error:', error);
        };

        return () => {
            eventSource.close();
        };
    }, [queryClient, user]);
};