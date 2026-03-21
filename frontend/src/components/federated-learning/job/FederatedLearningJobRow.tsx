import type {FederatedLearningJobDTO} from "@isin/federated-learning-management-service-client";
import {FederatedLearningJobStatusBadge} from "./FederatedLearningJobStatusBadge.tsx";

interface FederatedLearningJobRowProps {
    job: FederatedLearningJobDTO;
}

export const FederatedLearningJobRow = ({job}: FederatedLearningJobRowProps) => {
    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        }).format(date);
    };

    return (
        <tr className="hover:bg-base-200/50 transition-colors">
            <td>
        <span className="font-mono text-sm font-medium text-base-content">
          #{job.id}
        </span>
            </td>
            <td>
        <span
            className="text-sm text-base-content/70"
        >
          {job.celery_task_id}
        </span>
            </td>
            <td>
        <span className="text-sm text-base-content/70">
          {formatDate(job.created_at)}
        </span>
            </td>
            <td>
                <FederatedLearningJobStatusBadge status={job.status}/>
            </td>
        </tr>
    );
}
