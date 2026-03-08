import {useMemo, useState} from "react";
import type {FederatedLearningJobDTO} from "@isin/federated-learning-management-service-client";
import {FederatedLearningJobRow} from "./FederatedLearningJobRow";
import {ChevronDown, ChevronUp} from "lucide-react";

interface FederatedLearningJobsTableProps {
    jobs: FederatedLearningJobDTO[];
}

type SortField = "id" | "created_at";
type SortOrder = "asc" | "desc";

export const FederatedLearningJobsTable = ({jobs}: FederatedLearningJobsTableProps) => {
    const [sortField, setSortField] = useState<SortField>("id");
    const [sortOrder, setSortOrder] = useState<SortOrder>("desc");

    const handleSort = (field: SortField) => {
        if (sortField === field) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        } else {
            setSortField(field);
            setSortOrder("desc");
        }
    };

    const sortedJobs = useMemo(() => {
        return [...jobs].sort((a, b) => {
            let comparison = 0;

            if (sortField === "id") {
                comparison = a.id - b.id;
            } else if (sortField === "created_at") {
                comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
            }

            return sortOrder === "asc" ? comparison : -comparison;
        });
    }, [jobs, sortField, sortOrder]);

    const SortIcon = ({field}: { field: SortField }) => {
        if (sortField !== field) {
            return <ChevronUp size={16} className="opacity-30"/>;
        }
        return sortOrder === "asc" ? (
            <ChevronUp size={16} className="text-primary"/>
        ) : (
            <ChevronDown size={16} className="text-primary"/>
        );
    };

    return (
        <div className="overflow-x-auto rounded-lg bg-base-100 shadow">
            <table className="table w-full">
                <thead>
                <tr>
                    <th
                        className="text-base-content/70 cursor-pointer hover:bg-base-200 transition-colors select-none"
                        onClick={() => handleSort("id")}
                    >
                        <div className="flex items-center gap-2">
                            <span>ID</span>
                            <SortIcon field="id"/>
                        </div>
                    </th>
                    <th className="text-base-content/70">Celery Task ID</th>
                    <th
                        className="text-base-content/70 cursor-pointer hover:bg-base-200 transition-colors select-none"
                        onClick={() => handleSort("created_at")}
                    >
                        <div className="flex items-center gap-2">
                            <span>Created At</span>
                            <SortIcon field="created_at"/>
                        </div>
                    </th>
                    <th className="text-base-content/70">Status</th>
                </tr>
                </thead>
                <tbody>
                {sortedJobs.map((job) => (
                    <FederatedLearningJobRow key={job.id} job={job}/>
                ))}
                </tbody>
            </table>
        </div>
    );
}
