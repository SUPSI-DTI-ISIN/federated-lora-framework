import { useState } from "react";
import { useTranslation } from "react-i18next";
import { ChevronDown, ChevronUp, Network } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import type { FederatedLearningJobDTO } from "@isin/federated-learning-management-service-client";
import { FederatedLearningJobsTable } from "./FederatedLearningJobsTable.tsx";
import { EmptyState } from "../../common/EmptyState.tsx";

interface FederatedLearningJobsCardProps {
    jobs: FederatedLearningJobDTO[];
    searchQuery: string;
}

export const FederatedLearningJobsCard = ({ jobs, searchQuery }: FederatedLearningJobsCardProps) => {
    const { t } = useTranslation();
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className="bg-base-100 rounded-2xl border border-base-content/5 shadow-sm overflow-hidden">
            <button
                onClick={() => setIsOpen((prev) => !prev)}
                className="w-full flex items-center justify-between px-6 py-4 hover:bg-base-200/50 transition-colors cursor-pointer"
                aria-expanded={isOpen}
            >
                <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                        <Network size={20} />
                    </div>
                    <span className="font-bold text-base-content">
                        {t("federatedLearning.jobs.title")}
                    </span>
                    <span className="badge badge-primary badge-sm">{jobs.length}</span>
                </div>
                {isOpen ? <ChevronUp size={18} className="text-base-content/40" /> : <ChevronDown size={18} className="text-base-content/40" />}
            </button>

            <AnimatePresence initial={false}>
                {isOpen && (
                    <motion.div
                        key="jobs-body"
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2, ease: "easeInOut" }}
                        className="overflow-hidden"
                    >
                        <div className="px-6 pb-6 pt-2">
                            {jobs.length === 0 ? (
                                <EmptyState
                                    icon={Network}
                                    title={searchQuery ? t("federatedLearning.empty.noResults") : t("federatedLearning.empty.title")}
                                    description={searchQuery ? t("federatedLearning.empty.noResultsDescription") : t("federatedLearning.empty.description")}
                                />
                            ) : (
                                <FederatedLearningJobsTable jobs={jobs} />
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
