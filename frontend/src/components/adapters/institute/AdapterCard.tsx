import { Download, CheckCircle, Cloud } from "lucide-react";
import { useTranslation } from "react-i18next";
import type { AdapterDTO } from "@isin/model-service-client";
import { motion } from "framer-motion";
import { useReducedMotion } from "../../../hooks/useReducedMotion";
import {useState} from "react";
import {useSaveNewAdapter} from "../../../hooks/institute/model/useSaveNewAdapter.ts";
import toast from "react-hot-toast";

interface AdapterCardProps {
    adapter: AdapterDTO;
    modelKey: string;
}

export const AdapterCard = ({ adapter, modelKey }: AdapterCardProps) => {
    const { t } = useTranslation();
    const { version, available_local } = adapter;
    const prefersReducedMotion = useReducedMotion();

    const [isSavingNewAdapter, setIsSavingNewAdapter] = useState<boolean>(false);
    const {mutateAsync: saveNewAdapter} = useSaveNewAdapter();

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

    return (
        <motion.div
            layout
            initial={prefersReducedMotion ? {} : { opacity: 0, y: 10 }}
            animate={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
            exit={prefersReducedMotion ? {} : { opacity: 0, scale: 0.98 }}
            whileHover={prefersReducedMotion ? {} : { y: -2 }}
            transition={prefersReducedMotion ? { duration: 0 } : { duration: 0.2 }}
            className="group w-full bg-base-100 p-4 sm:p-5 rounded-2xl border border-base-content/5 hover:border-info/30 hover:shadow-xl hover:shadow-info/5 transition-all duration-300"
        >
            <div className="flex flex-row items-center justify-between gap-6">

                {/* Left Side: Version Indicator */}
                <div className="flex items-center gap-5 min-w-0">
                    <div className="flex flex-col items-center justify-center w-14 h-14 shrink-0 rounded-xl bg-base-200 text-base-content group-hover:bg-info group-hover:text-info-content transition-all duration-500 shadow-inner font-black">
                        <span className="text-[9px] uppercase opacity-50 mb-0.5 tracking-tighter">Ver</span>
                        <span className="text-xl leading-none">{version}</span>
                    </div>

                    <div className="truncate">
                        <h3 className="text-lg font-bold text-base-content truncate group-hover:text-info transition-colors">
                            {t("adapters.card.title", { version })}
                        </h3>
                        <div className="flex items-center gap-3 mt-1">
                            {available_local ? (
                                <span className="flex items-center gap-1.5 text-xs font-bold text-success uppercase tracking-wide" role="status" aria-label="Available locally">
                                    <CheckCircle size={14} strokeWidth={3} aria-hidden="true" />
                                    {t("adapters.local")}
                                </span>
                            ) : (
                                <span className="flex items-center gap-1.5 text-xs font-bold text-info uppercase tracking-wide" role="status" aria-label="Available remotely">
                                    <Cloud size={14} strokeWidth={3} aria-hidden="true" />
                                    {t("adapters.notLocal")}
                                </span>
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Side: Action Button */}
                <div className="flex items-center shrink-0">
                    {available_local ? (
                        <div className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-xl bg-success/5 text-success font-bold text-sm border border-success/10" role="status">
                            <CheckCircle size={16} aria-hidden="true" />
                            {t("adapters.installed")}
                        </div>
                    ) : (
                        <button
                            onClick={() => handleDownload(version)}
                            disabled={isSavingNewAdapter}
                            className={`
                                btn btn-md sm:btn-lg rounded-2xl min-h-[44px] min-w-[44px]
                                ${isSavingNewAdapter ? 'btn-ghost' : 'btn-info'} 
                                shadow-lg shadow-info/20 hover:scale-105 transition-all
                                px-6
                            `}
                            aria-label={`Download adapter version ${version}`}
                        >
                            {isSavingNewAdapter ? (
                                <span className="loading loading-spinner" aria-label="Downloading" />
                            ) : (
                                <>
                                    <Download size={20} className="mr-2" aria-hidden="true" />
                                    <span className="hidden sm:inline">{t("adapters.download")}</span>
                                </>
                            )}
                        </button>
                    )}
                </div>
            </div>
        </motion.div>
    );
};