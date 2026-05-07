import type {InstituteTrainingParticipationDTO} from "@isin/institute-service-client";
import {useTranslation} from "react-i18next";
import {useMemo, useState} from "react";
import {ChevronDown, ChevronUp} from "lucide-react";
import {InstitutesTrainingParticipationRow} from "./InstitutesTrainingParticipationRow.tsx";

interface InstitutesTrainingParticipationTableProps {
    institutesTrainingParticipation: InstituteTrainingParticipationDTO[]
}

type SortField = "id" | "institute_name" | "trainable_samples_number";
type SortOrder = "asc" | "desc";

export const InstitutesTrainingParticipationTable = ({institutesTrainingParticipation}: InstitutesTrainingParticipationTableProps) => {
    const {t} = useTranslation();
    const [sortField, setSortField] = useState<SortField>("id");
    const [sortOrder, setSortOrder] = useState<SortOrder>("asc");

    const handleSort = (field: SortField) => {
        if (sortField === field) {
            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
        } else {
            setSortField(field);
            setSortOrder("desc");
        }
    };

    const sorted = useMemo(() => {
        return [...institutesTrainingParticipation].sort((a, b) => {
            let comparison = 0;
            if (sortField === "id") {
                comparison = a.id - b.id;
            } else if (sortField === "institute_name") {
                comparison = a.institute_name.localeCompare(b.institute_name);
            } else if (sortField === "trainable_samples_number") {
                const aVal = a.trainable_samples_number ?? -1;
                const bVal = b.trainable_samples_number ?? -1;
                comparison = aVal - bVal;
            }
            return sortOrder === "asc" ? comparison : -comparison;
        });
    }, [institutesTrainingParticipation, sortField, sortOrder]);

    const SortIcon = ({field}: { field: SortField }) => {
        if (sortField !== field) return <ChevronUp size={14} className="opacity-25"/>;
        return sortOrder === "asc"
            ? <ChevronUp size={14} className="text-secondary"/>
            : <ChevronDown size={14} className="text-secondary"/>;
    };

    return (
        <div className="overflow-x-auto rounded-lg">
            <table className="table w-full text-sm">
                <thead>
                <tr>
                    <th className="text-base-content/60 cursor-pointer hover:bg-base-200 transition-colors select-none" onClick={() => handleSort("institute_name")}>
                        <div className="flex items-center gap-1">
                            {t("federatedLearning.participation.col.name")} <SortIcon field="institute_name"/>
                        </div>
                    </th>
                    <th className="text-base-content/60 cursor-pointer hover:bg-base-200 transition-colors select-none" onClick={() => handleSort("id")}>
                        <div className="flex items-center gap-1">
                            ID <SortIcon field="id"/>
                        </div>
                    </th>
                    <th className="text-base-content/60 cursor-pointer hover:bg-base-200 transition-colors select-none" onClick={() => handleSort("trainable_samples_number")}>
                        <div className="flex items-center gap-1">
                            {t("federatedLearning.participation.col.samples")} <SortIcon
                            field="trainable_samples_number"/>
                        </div>
                    </th>
                    <th className="text-base-content/60">
                        {t("federatedLearning.participation.col.status")}
                    </th>
                </tr>
                </thead>
                <tbody>
                {sorted.map((instituteTrainingParticipation) => (
                    <InstitutesTrainingParticipationRow key={instituteTrainingParticipation.id} instituteTrainingParticipation={instituteTrainingParticipation} />
                ))}
                </tbody>
            </table>
        </div>
    );
};