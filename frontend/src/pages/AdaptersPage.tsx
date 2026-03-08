import {useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import toast from "react-hot-toast";
import {AdapterFilterBar} from "../components/adapters/AdapterFilterBar";
import {AdaptersList} from "../components/adapters/institute/AdaptersList.tsx";
import {useGetAllAvailableAdapters} from "../hooks/institute/model/useGetAllAvailableAdapters.ts";
import {getModelKey} from "../utils/envUtils.ts";
import {useSaveNewAdapter} from "../hooks/institute/model/useSaveNewAdapter.ts";
import type {AdapterDTO} from "@isin/model-service-client";
import { motion } from "framer-motion";
import {Cpu} from "lucide-react";
import {LoadingSkeleton} from "../components/common/LoadingSkeleton.tsx";
import {PageHeader} from "../components/common/PageHeader.tsx";
import {EmptyState} from "../components/common/EmptyState.tsx";
import {useReducedMotion} from "../hooks/useReducedMotion";

export const AdaptersPage = () => {
    const {t} = useTranslation();
    const modelKey = getModelKey();
    const prefersReducedMotion = useReducedMotion();
    const {
        data: availableAdapters,
        isLoading: isLoadingAdapters,
        error: errorLoadingAdapters
    } = useGetAllAvailableAdapters(modelKey);

    const [isSavingNewAdapter, setIsSavingNewAdapter] = useState<boolean>(false);
    const {mutateAsync: saveNewAdapter} = useSaveNewAdapter();

    const [query, setQuery] = useState("");
    const [localOnly, setLocalOnly] = useState(false);

    const adapters = useMemo(() => availableAdapters?.adapters ?? [], [availableAdapters]);

    const filtered = adapters.filter((adapter: AdapterDTO) => {
        const matchQuery = adapter?.version?.toString().includes(query.toLowerCase()) || (adapter?.version && `v${adapter.version}`.includes(query));
        const matchLocal = !localOnly || adapter.available_local;
        return matchQuery && matchLocal;
    });

    const handleDownload = async (adapterVersion: number) => {
        try {
            setIsSavingNewAdapter(true);
            toast.loading(t("adapters.toast.downloading"), {id: "adapter-download"});
            await saveNewAdapter({modelKey, adapterVersion});
            toast.success(t("adapters.toast.downloaded"), {id: "adapter-download"});
        } catch (err: any) {
            console.error(err);
            toast.error(t("adapters.toast.error"), {id: "adapter-download"});
        } finally {
            setIsSavingNewAdapter(false);
        }
    };

    if (isLoadingAdapters) {
        return (
            <motion.div
                initial={prefersReducedMotion ? {} : {opacity: 0, y: 12}}
                animate={prefersReducedMotion ? {} : {opacity: 1, y: 0}}
                transition={prefersReducedMotion ? {duration: 0} : {duration: 0.25}}
                className="min-h-screen bg-base-100 py-12 px-4 sm:px-8"
            >
                <div className="max-w-7xl mx-auto">
                    <PageHeader
                        icon={Cpu}
                        title={t("adapters.title")}
                        subtitle={t("adapters.subtitle")}
                    />
                    <LoadingSkeleton variant="card" count={5} />
                </div>
            </motion.div>
        );
    }

    if (errorLoadingAdapters) {
        return (
            <motion.div
                initial={prefersReducedMotion ? {} : {opacity: 0, y: 12}}
                animate={prefersReducedMotion ? {} : {opacity: 1, y: 0}}
                transition={prefersReducedMotion ? {duration: 0} : {duration: 0.25}}
                className="min-h-screen bg-base-100 py-12 px-4 sm:px-8"
            >
                <div className="max-w-7xl mx-auto">
                    <PageHeader
                        icon={Cpu}
                        title={t("adapters.title")}
                        subtitle={t("adapters.subtitle")}
                    />
                    <div role="alert" className="alert alert-error">
                        <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span>{t("adapters.errorFetch")}</span>
                    </div>
                </div>
            </motion.div>
        );
    }

    return (
        <motion.div
            initial={prefersReducedMotion ? {} : {opacity: 0, y: 12}}
            animate={prefersReducedMotion ? {} : {opacity: 1, y: 0}}
            transition={prefersReducedMotion ? {duration: 0} : {duration: 0.25}}
            className="min-h-screen bg-base-100 py-12 px-4 sm:px-8 relative"
        >
            <div className="relative z-10 max-w-7xl mx-auto">
                {/* Header */}
                <PageHeader
                    icon={Cpu}
                    title={t("adapters.title")}
                    subtitle={t("adapters.subtitle")}
                />

                {/* Filter Bar */}
                <div className="bg-base-200/50 p-2 rounded-2xl border border-base-content/5 mb-6">
                    <AdapterFilterBar
                        query={query}
                        onQueryChange={setQuery}
                        localOnly={localOnly}
                        onLocalOnlyChange={setLocalOnly}
                    />
                </div>

                {/* Adapters List or Empty State */}
                {filtered.length === 0 ? (
                    <EmptyState
                        icon={Cpu}
                        title={t("adapters.empty")}
                        description={t("adapters.emptyDescription")}
                    />
                ) : (
                    <AdaptersList
                        adapters={filtered}
                        onDownload={handleDownload}
                        isDownloading={isSavingNewAdapter}
                    />
                )}
            </div>
        </motion.div>
    );
};