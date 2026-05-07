import {useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import {AdaptersList} from "../components/adapters/institute/AdaptersList.tsx";
import {useGetAllAvailableAdapters} from "../hooks/institute/model/useGetAllAvailableAdapters.ts";
import {getModelKey} from "../utils/envUtils.ts";
import type {AdapterDTO} from "@isin/model-service-client";
import {motion} from "framer-motion";
import {Cpu} from "lucide-react";
import {LoadingSkeleton} from "../components/common/LoadingSkeleton.tsx";
import {EmptyState} from "../components/common/EmptyState.tsx";
import {SearchBar} from "../components/common/SearchBar.tsx";
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

    const [query, setQuery] = useState("");
    const [localOnly, setLocalOnly] = useState(false);

    const adapters = useMemo(() => availableAdapters?.adapters ?? [], [availableAdapters]);

    const filtered = adapters.filter((adapter: AdapterDTO) => {
        const matchQuery = adapter?.version?.toString().includes(query.toLowerCase()) || (adapter?.version && `v${adapter.version}`.includes(query));
        const matchLocal = !localOnly || adapter.available_local;
        return matchQuery && matchLocal;
    });

    if (isLoadingAdapters) {
        return (
            <motion.div
                initial={prefersReducedMotion ? {} : {opacity: 0, y: 12}}
                animate={prefersReducedMotion ? {} : {opacity: 1, y: 0}}
                transition={prefersReducedMotion ? {duration: 0} : {duration: 0.25}}
                className="min-h-screen bg-base-100 py-12 px-4 sm:px-8"
            >
                <div className="max-w-7xl mx-auto">
                    <div className="flex items-center gap-5 mb-8">
                        <div
                            className="flex h-16 w-16 items-center justify-center bg-info/10 rounded-2xl text-info shadow-inner">
                            <Cpu size={36}/>
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
                    <LoadingSkeleton variant="card" count={5}/>
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
                    <div className="flex items-center gap-5 mb-8">
                        <div
                            className="flex h-16 w-16 items-center justify-center bg-info/10 rounded-2xl text-info shadow-inner">
                            <Cpu size={36}/>
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
                    <div role="alert" className="alert alert-error">
                        <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none"
                             viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                                  d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
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
                <div className="flex items-center gap-5 mb-8">
                    <div
                        className="flex h-16 w-16 items-center justify-center bg-info/10 rounded-2xl text-info shadow-inner">
                        <Cpu size={36}/>
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

                {/* Search Bar and Filter */}
                <div className="flex flex-col sm:flex-row gap-4 mb-6">
                    <SearchBar
                        value={query}
                        onChange={setQuery}
                        placeholder={t("adapters.filter.searchPlaceholder")}
                    />

                    <label className="flex items-center gap-2 cursor-pointer whitespace-nowrap">
                        <input
                            type="checkbox"
                            checked={localOnly}
                            onChange={(e) => setLocalOnly(e.target.checked)}
                            className="checkbox checkbox-primary"
                        />
                        <span className="label-text">{t("adapters.filter.localOnly")}</span>
                    </label>
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
                        modelKey={modelKey}
                    />
                )}
            </div>
        </motion.div>
    );
};