import {useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import toast from "react-hot-toast";
import {AdapterFilterBar} from "../components/adapters/AdapterFilterBar";
import {AdaptersList} from "../components/adapters/AdaptersList";
import {useGetAllAvailableAdapters} from "../hooks/model/useGetAllAvailableAdapters.ts";
import {getModelKey} from "../utils/envUtils.ts";
import {useSaveNewAdapter} from "../hooks/model/useSaveNewAdapter.ts";
import type {AdapterDTO} from "@isin/model-service-client";

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

    if (errorLoadingAdapters || !adapters) {
        return (
            <div className="card bg-base-100 shadow p-4 text-red-600">
                <div>{t("adapters.errorFetch")}</div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-linear-to-br from-base-100 via-base-200 to-base-100 py-8 px-4">
            <div className="max-w-7xl mx-auto">
                <div className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div>
                        <h1 className="text-3xl font-bold">{t("adapters.title")}</h1>
                        <p className="text-base-content/70">{t("adapters.subtitle")}</p>
                    </div>

                    <div className="w-full md:w-auto">
                        <AdapterFilterBar
                            query={query}
                            onQueryChange={setQuery}
                            localOnly={localOnly}
                            onLocalOnlyChange={setLocalOnly}
                        />
                    </div>
                </div>

                <AdaptersList
                    adapters={filtered}
                    onDownload={handleDownload}
                    isDownloading={isSavingNewAdapter}
                />
            </div>
        </div>
    );
};