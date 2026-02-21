import {useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import toast from "react-hot-toast";
import {AdapterFilterBar} from "../components/adapters/AdapterFilterBar";
import {AdaptersList} from "../components/adapters/AdaptersList";
import {useGetAllAvailableAdapters} from "../hooks/institute/model/useGetAllAvailableAdapters.ts";
import {getModelKey} from "../utils/envUtils.ts";
import {useSaveNewAdapter} from "../hooks/institute/model/useSaveNewAdapter.ts";
import type {AdapterDTO} from "@isin/model-service-client";
import { motion } from "framer-motion";
import {Cpu} from "lucide-react";

export const AdaptersPage = () => {
    const {t} = useTranslation();
    const modelKey = getModelKey();
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

                    <div className="bg-base-200/50 p-2 rounded-2xl border border-base-content/5">
                        <AdapterFilterBar
                            query={query}
                            onQueryChange={setQuery}
                            localOnly={localOnly}
                            onLocalOnlyChange={setLocalOnly}
                        />
                    </div>
                </motion.div>

                <AdaptersList
                    adapters={filtered}
                    onDownload={handleDownload}
                    isDownloading={isSavingNewAdapter}
                />
            </div>
        </div>
    );
};