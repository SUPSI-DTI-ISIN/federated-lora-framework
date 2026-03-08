import {useEffect, useState} from "react";
import {useTranslation} from "react-i18next";
import {motion} from "framer-motion";
import {Network} from "lucide-react";
import {useAuthWrapper} from "../hooks/auth/useAuthWrapper.ts";
import {useNavigate} from "react-router-dom";
import {useGetAllFederatedLearningJobs} from "../hooks/department/federated-learning/useGetAllFederatedLearningJobs.ts";
import {useFederatedLearningJobSse} from "../hooks/department/federated-learning/useFederatedLearningJobSse.ts";
import {LoadingSkeleton} from "../components/common/LoadingSkeleton.tsx";
import {FederatedLearningJobsTable} from "../components/federated-learning/FederatedLearningJobsTable.tsx";
import {FederatedLearningActions} from "../components/federated-learning/FederatedLearningActions.tsx";
import {EmptyState} from "../components/common/EmptyState.tsx";
import {SearchBar} from "../components/common/SearchBar.tsx";

export const FederatedLearningJobsPage = () => {
    useFederatedLearningJobSse();
    const {t} = useTranslation();
    const {isDepartmentAdmin} = useAuthWrapper();
    const navigate = useNavigate();
    const [searchQuery, setSearchQuery] = useState("");

    const {
        data: jobs,
        isLoading: isLoadingJobs,
        error: errorLoadingJobs,
    } = useGetAllFederatedLearningJobs();

    useEffect(() => {
        if (!isDepartmentAdmin) navigate("/");
    }, [isDepartmentAdmin, navigate]);

    if (isLoadingJobs) {
        return <LoadingSkeleton variant="table" count={5}/>;
    }

    if (errorLoadingJobs) {
        return (
            <div className="card bg-base-100 shadow p-4 text-red-600">
                <div>{t("federatedLearning.errorFetch")}</div>
            </div>
        );
    }

    const filteredJobs = (jobs || []).filter((job) => {
        const query = searchQuery.trim().toLowerCase();
        if (!query) return true;
        return (
            job.id.toString().includes(query) ||
            job.celery_task_id.toLowerCase().includes(query)
        );
    });

    return (
        <div className="min-h-screen bg-base-100 py-12 px-4 sm:px-8 relative">
            <div className="relative z-10 max-w-7xl mx-auto">
                <motion.div
                    initial={{opacity: 0, y: -10}}
                    animate={{opacity: 1, y: 0}}
                    className="flex items-center justify-between gap-5 mb-8"
                >
                    <div className="flex items-center gap-5">
                        <div
                            className="flex h-16 w-16 items-center justify-center bg-secondary/10 rounded-2xl text-secondary shadow-inner">
                            <Network size={36}/>
                        </div>
                        <div>
                            <h1 className="text-4xl font-black tracking-tight text-base-content leading-none mb-2">
                                {t("federatedLearning.title")}
                            </h1>
                            <p className="text-lg text-base-content/60 font-medium">
                                {t("federatedLearning.subtitle")}
                            </p>
                        </div>
                    </div>

                    <div className="shrink-0">
                        <FederatedLearningActions/>
                    </div>
                </motion.div>

                <div className="mb-6">
                    <SearchBar
                        value={searchQuery}
                        onChange={setSearchQuery}
                        placeholder={t("federatedLearning.search.placeholder")}
                    />
                </div>

                {filteredJobs.length === 0 ? (
                    <EmptyState
                        icon={Network}
                        title={
                            searchQuery
                                ? t("federatedLearning.empty.noResults")
                                : t("federatedLearning.empty.title")
                        }
                        description={
                            searchQuery
                                ? t("federatedLearning.empty.noResultsDescription")
                                : t("federatedLearning.empty.description")
                        }
                    />
                ) : (
                    <FederatedLearningJobsTable jobs={filteredJobs}/>
                )}
            </div>
        </div>
    );
};

