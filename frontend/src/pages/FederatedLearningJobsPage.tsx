import {useEffect, useState} from "react";
import {useTranslation} from "react-i18next";
import {motion} from "framer-motion";
import {Network} from "lucide-react";
import {useAuthWrapper} from "../hooks/auth/useAuthWrapper.ts";
import {useNavigate} from "react-router-dom";
import {useGetAllFederatedLearningJobs} from "../hooks/department/federated-learning/useGetAllFederatedLearningJobs.ts";
import {useFederatedLearningJobSse} from "../hooks/department/federated-learning/useFederatedLearningJobSse.ts";
import {LoadingSkeleton} from "../components/common/LoadingSkeleton.tsx";
import {FederatedLearningActions} from "../components/federated-learning/FederatedLearningActions.tsx";
import {SearchBar} from "../components/common/SearchBar.tsx";
import {InstituteTrainingParticipationCard} from "../components/federated-learning/institute-participation/InstituteTrainingParticipationCard.tsx";
import {FederatedLearningJobsCard} from "../components/federated-learning/job/FederatedLearningJobsCard.tsx";

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

                <div className="flex flex-col gap-4">
                    <InstituteTrainingParticipationCard />
                    <FederatedLearningJobsCard jobs={filteredJobs} searchQuery={searchQuery} />
                </div>
            </div>
        </div>
    );
};

