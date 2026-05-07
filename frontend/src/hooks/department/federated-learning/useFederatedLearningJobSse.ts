import { useEffect } from "react";
import {useQueryClient} from "@tanstack/react-query";
import {getFederatedLearningJobSseUrl} from "../../../utils/sse/sseUrls.ts";
import type {FederatedLearningJobDTO} from "@isin/federated-learning-management-service-client";

export const useFederatedLearningJobSse = () => {
    const queryClient = useQueryClient();

    useEffect(() => {
        const eventSource = new EventSource(getFederatedLearningJobSseUrl());

        eventSource.addEventListener("federated_learning_job_update", (event) => {
            try {
                const parsed = JSON.parse(event.data);
                console.log(parsed);

                queryClient.setQueryData<FederatedLearningJobDTO[]>(
                    ['federated-learning-jobs'],
                    (oldJobs) => {
                        if (!oldJobs) return oldJobs;

                        return oldJobs.map((job) =>
                            job.celery_task_id === parsed.job_id
                                ? { ...job, status: parsed.result_type }
                                : job
                        );
                    }
                );
                queryClient.invalidateQueries({queryKey: ["department-adapters"]})
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
    }, [queryClient]);
};