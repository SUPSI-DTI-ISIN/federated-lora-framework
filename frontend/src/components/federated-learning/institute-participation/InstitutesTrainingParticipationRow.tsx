import type {InstituteTrainingParticipationDTO} from "@isin/institute-service-client";
import {useTranslation} from "react-i18next";
import {WifiOff} from "lucide-react";
import {formatEnum} from "../../../utils/enumUtils.ts";

interface InstitutesTrainingParticipationTableRowProps {
    instituteTrainingParticipation: InstituteTrainingParticipationDTO
}

export const InstitutesTrainingParticipationRow = ({instituteTrainingParticipation}: InstitutesTrainingParticipationTableRowProps) => {
    const {t} = useTranslation();

    return (
        <tr key={instituteTrainingParticipation.id} className="hover:bg-base-200/40 transition-colors">
            <td className="font-mono text-base-content/50">#{instituteTrainingParticipation.id}</td>
            <td className="font-medium text-base-content">{instituteTrainingParticipation.institute_name}</td>
            <td className="font-semibold text-secondary">
                {instituteTrainingParticipation.is_reachable ? (instituteTrainingParticipation.trainable_samples_number ?? 0) : "—"}
            </td>
            <td>
                {instituteTrainingParticipation.is_reachable ? (
                    <span className="badge badge-success rounded-full text-xs font-medium px-3 py-2">
                                        {formatEnum(t("federatedLearning.participation.reachable"))}
                                    </span>
                ) : (
                    <span className="badge badge-error rounded-full text-xs font-medium px-3 py-2">
                                        <WifiOff size={14}/>
                        {formatEnum(t("federatedLearning.participation.unreachable"))}
                                    </span>
                )}
            </td>
        </tr>
    );
};