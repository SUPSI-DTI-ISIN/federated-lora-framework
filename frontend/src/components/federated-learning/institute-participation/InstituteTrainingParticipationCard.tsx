import {useState} from "react";
import {useTranslation} from "react-i18next";
import {
    AlertCircle
} from "lucide-react";
import {motion, AnimatePresence} from "framer-motion";
import {
    useGetInstitutesTrainingParticipation
} from "../../../hooks/department/institutes/useGetInstitutesTrainingParticipation.ts";
import {LoadingSkeleton} from "../../common/LoadingSkeleton.tsx";
import {InstitutesTrainingParticipationTable} from "./InstitutesTrainingParticipationTable.tsx";
import {InstituteTrainingParticipationCardHeader} from "./InstituteTrainingParticipationCardHeader.tsx";
import {InstitutesTrainingParticipationChart} from "./InstitutesTrainingParticipationChart.tsx";

export const InstituteTrainingParticipationCard = () => {
    const {t} = useTranslation();
    const [isOpen, setIsOpen] = useState(false);
    const [viewMode, setViewMode] = useState<"table" | "chart">("table");

    const {
        data: institutesTrainingParticipation,
        isLoading: isLoadingInstitutesTrainingParticipation,
        error: errorLoadingInstitutesTrainingParticipation,
    } = useGetInstitutesTrainingParticipation();

    const displayData = institutesTrainingParticipation ?? [];

    return (
        <div className="bg-base-100 rounded-2xl border border-base-content/5 shadow-sm overflow-hidden">
            <InstituteTrainingParticipationCardHeader isOpen={isOpen} setIsOpen={setIsOpen} viewMode={viewMode} setViewMode={setViewMode} institutesTrainingParticipationLen={displayData.length} />

            <AnimatePresence initial={false}>
                {isOpen && (
                    <motion.div
                        key="participation-body"
                        initial={{height: 0, opacity: 0}}
                        animate={{height: "auto", opacity: 1}}
                        exit={{height: 0, opacity: 0}}
                        transition={{duration: 0.2, ease: "easeInOut"}}
                        className="overflow-hidden"
                    >
                        <div className="px-6 pb-6 pt-2">
                            {isLoadingInstitutesTrainingParticipation && (
                                <LoadingSkeleton variant="list" count={4}/>
                            )}
                            {errorLoadingInstitutesTrainingParticipation && (
                                <div role="alert" className="alert alert-error">
                                    <AlertCircle size={20}/>
                                    <span>{t("federatedLearning.participation.error")}</span>
                                </div>
                            )}
                            {!isLoadingInstitutesTrainingParticipation &&
                                !errorLoadingInstitutesTrainingParticipation &&
                                displayData.length === 0 && (
                                    <p className="text-sm text-base-content/50 text-center py-4">
                                        {t("federatedLearning.participation.empty")}
                                    </p>
                                )}
                            {displayData.length > 0 && (
                                <AnimatePresence mode="wait">
                                    <motion.div
                                        key={viewMode}
                                        initial={{opacity: 0, y: 6}}
                                        animate={{opacity: 1, y: 0}}
                                        exit={{opacity: 0, y: -6}}
                                        transition={{duration: 0.15}}
                                    >
                                        {viewMode === "table"
                                            ? <InstitutesTrainingParticipationTable institutesTrainingParticipation={displayData}/>
                                            : <InstitutesTrainingParticipationChart institutesTrainingParticipation={displayData}/>}
                                    </motion.div>
                                </AnimatePresence>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
