import {useTranslation} from "react-i18next";
import {WifiOff} from "lucide-react";
import type {InstituteTrainingParticipationDTO} from "@isin/institute-service-client";

interface InstitutesTrainingParticipationChartCustomTooltipProps {
    active?: boolean;
    payload?: { payload: InstituteTrainingParticipationDTO }[];
}

export const InstitutesTrainingParticipationChartCustomTooltip = ({active, payload}: InstitutesTrainingParticipationChartCustomTooltipProps) => {
    const {t} = useTranslation();
    if (!active || !payload?.length) return null;
    const entry = payload[0].payload;

    return (
        <div className="bg-base-100 border border-base-content/10 rounded-xl shadow-lg px-4 py-2 text-sm">
            {entry.is_reachable ? (
                <span className="font-semibold text-base-content">
                    {entry.trainable_samples_number ?? 0}{" "}
                    <span className="font-normal text-base-content/80">
                        {t("federatedLearning.participation.samples")}
                    </span>
                </span>
            ) : (
                <span className="text-error flex items-center gap-1">
                    <WifiOff size={14}/> {t("federatedLearning.participation.unreachable")}
                </span>
            )}
        </div>
    );
}
