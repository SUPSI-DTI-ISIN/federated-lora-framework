import {useEffect, useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import {getModelKey} from "../utils/envUtils.ts";
import {motion} from "framer-motion";
import {Cpu, Play, ExternalLink, Loader2} from "lucide-react";
import {useAuthWrapper} from "../hooks/auth/useAuthWrapper.ts";
import {useNavigate} from "react-router-dom";
import {useGetAllDepartmentAdapters} from "../hooks/department/mlflow/useGetAllDepartmentAdapters.ts";
import {DepartmentAdaptersList} from "../components/adapters/department/DepartmentAdaptersList.tsx";
import {useFederatedLearningJobSse} from "../hooks/department/federated-learning/useFederatedLearningJobSse.ts";
import {LoadingSkeleton} from "../components/common/LoadingSkeleton.tsx";
import {SearchBar} from "../components/common/SearchBar.tsx";
import {useStartFederatedLearning} from "../hooks/department/federated-learning/useStartFederatedLearning.ts";
import {getFlowerCeleryJobsUrl} from "../utils/envUtils.ts";
import toast from "react-hot-toast";

export const AdaptersAdminPage = () => {
    useFederatedLearningJobSse();
    const {t} = useTranslation();
    const {isDepartmentAdmin} = useAuthWrapper();
    const navigate = useNavigate();
    const modelKey = getModelKey();

    const {
        data: availableAdapters,
        isLoading: isLoadingAdapters,
        error: errorLoadingAdapters
    } = useGetAllDepartmentAdapters(modelKey);

    const { mutateAsync: startFederatedLearning } = useStartFederatedLearning();
    const [isStarting, setIsStarting] = useState<boolean>(false);

    const [query, setQuery] = useState("");

    const adapters = useMemo(() => availableAdapters?.adapters_version ?? [], [availableAdapters]);

    const filtered = adapters.filter((adapterVersion: number) => {
        return adapterVersion?.toString().includes(query.toLowerCase()) || (adapterVersion && `v${adapterVersion}`.includes(query));
    });

    useEffect(() => {
        if(!isDepartmentAdmin)
            navigate("/")
    }, [isDepartmentAdmin]);

    const handleStartFL = async () => {
        try {
            setIsStarting(true);
            await startFederatedLearning();
            toast.success(t("adapters.admin.fl.startSuccess"));
        } catch (err: any) {
            console.error(err);
            toast.error(t("adapters.admin.fl.startError"));
        } finally {
            setIsStarting(false);
        }
    };

    if (isLoadingAdapters) {
        return <LoadingSkeleton variant="list" count={5} />;
    }

    if (errorLoadingAdapters) {
        return (
            <div className="card bg-base-100 shadow p-4 text-red-600">
                <div>{t("adapters.errorFetch")}</div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-base-100 py-12 px-4 sm:px-8 relative">

            <div className="relative z-10 max-w-7xl mx-auto">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 mb-12"
                >
                    <div className="flex items-center gap-5">
                        <div className="flex h-16 w-16 items-center justify-center bg-info/10 rounded-2xl text-info shadow-inner">
                            <Cpu size={36} />
                        </div>
                        <div>
                            <h1 className="text-4xl font-black tracking-tight text-base-content leading-none mb-2">
                                {t("adapters.title")}
                            </h1>
                            <p className="text-lg text-base-content/60 font-medium">
                                {t("adapters.subtitle")}
                            </p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3">
                        <button
                            onClick={handleStartFL}
                            disabled={isStarting}
                            className="btn btn-primary gap-2"
                        >
                            {isStarting ? (
                                <Loader2 size={18} className="animate-spin" />
                            ) : (
                                <Play size={18} fill="currentColor" />
                            )}
                            <span>{t("adapters.admin.fl.start")}</span>
                        </button>

                        <a
                            href={getFlowerCeleryJobsUrl()}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn btn-ghost btn-square"
                            title={t("adapters.admin.fl.trackJobs")}
                        >
                            <ExternalLink size={20} />
                        </a>
                    </div>
                </motion.div>

                {/* Search Bar */}
                <div className="mb-6">
                    <SearchBar
                        value={query}
                        onChange={setQuery}
                        placeholderKey="adapters.filter.searchPlaceholder"
                    />
                </div>

                <DepartmentAdaptersList
                    adapters={filtered}
                />
            </div>
        </div>
    );
};