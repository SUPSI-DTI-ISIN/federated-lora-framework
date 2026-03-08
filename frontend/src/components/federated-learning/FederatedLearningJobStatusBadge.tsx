interface FederatedLearningJobStatusBadgeProps {
    status: string;
}

export const FederatedLearningJobStatusBadge = ({status}: FederatedLearningJobStatusBadgeProps) => {
    const getStatusVariant = (status: string): string => {
        const lowerStatus = status.toLowerCase();

        if (lowerStatus.includes("success") || lowerStatus.includes("completed")) {
            return "badge-success";
        }

        if (lowerStatus.includes("failure") || lowerStatus.includes("failed") || lowerStatus.includes("error")) {
            return "badge-error";
        }

        if (lowerStatus.includes("progress") || lowerStatus.includes("running") || lowerStatus.includes("pending")) {
            return "badge-info";
        }

        return "badge-neutral";
    };

    return (
        <span
            className={`badge ${getStatusVariant(status)} rounded-full text-xs font-medium px-3 py-2`}
            role="status"
            aria-label={`Status: ${status}`}
        >
      {status}
    </span>
    );
}
