import {useEffect, useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import {AdapterFilterBar} from "../components/adapters/AdapterFilterBar";
import {getModelKey} from "../utils/envUtils.ts";
import {motion} from "framer-motion";
import {Cpu} from "lucide-react";
import {useAuthWrapper} from "../hooks/auth/useAuthWrapper.ts";
import {useNavigate} from "react-router-dom";
import {useGetAllDepartmentAdapters} from "../hooks/department/mlflow/useGetAllDepartmentAdapters.ts";
import {DepartmentAdaptersList} from "../components/adapters/department/DepartmentAdaptersList.tsx";
import {useFederatedLearningJobSse} from "../hooks/department/federated-learning/useFederatedLearningJobSse.ts";
import {FederatedLearningActions} from "../components/adapters/department/FederatedLearningActions.tsx";

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

    const [query, setQuery] = useState("");

    const adapters = useMemo(() => availableAdapters?.adapters_version ?? [], [availableAdapters]);

    const filtered = adapters.filter((adapterVersion: number) => {
        return adapterVersion?.toString().includes(query.toLowerCase()) || (adapterVersion && `v${adapterVersion}`.includes(query));
    });

    useEffect(() => {
        if(!isDepartmentAdmin)
            navigate("/")
    }, [isDepartmentAdmin]);

    if (isLoadingAdapters) {
        return (
            <div className="space-y-3">
                {/* skeleton placeholders */}
                {[1, 2, 3].map((i) => (
                    <div key={i} className="card bg-base-100 shadow animate-pulse h-20"/>
                ))}
            </div>
        )
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
                    className="flex flex-col lg:flex-row lg:items-center justify-between gap-8 mb-12"
                >
                    <div className="flex items-center gap-5">
                        <div className="flex h-16 w-16 items-center justify-center bg-secondary/10 rounded-2xl text-secondary shadow-inner">
                            <Cpu size={36} /> {/* Microchip/Cpu icon */}
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

                    <div className="flex items-center bg-base-200/50 p-2 rounded-2xl border border-base-content/5 shadow-sm">
                        <AdapterFilterBar
                            query={query}
                            onQueryChange={setQuery}
                        />

                        <FederatedLearningActions />
                    </div>
                </motion.div>

                <DepartmentAdaptersList
                    adapters={filtered}
                />
            </div>
        </div>
    );
};