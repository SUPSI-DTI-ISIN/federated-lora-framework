import { useEffect } from "react";
import {useQueryClient} from "@tanstack/react-query";
import {getFederatedLearningJobSseUrl} from "../../../utils/sse/sseUrls.ts";

export const useFederatedLearningJobSse = () => {
    const queryClient = useQueryClient();

    useEffect(() => {
        const eventSource = new EventSource(getFederatedLearningJobSseUrl());

        eventSource.addEventListener("federated_learning_job_update", (event) => {
            try {
                const parsed = JSON.parse(event.data);
                console.log(parsed);
            } catch (err) {
                console.error("Invalid SSE payload", err);
            }

            queryClient.invalidateQueries({queryKey: ["department-adapters"]})
        })

        eventSource.onerror = (error) => {
            console.error('SSE connection error:', error);
        };

        return () => {
            eventSource.close();
        };
    }, [queryClient]);
};