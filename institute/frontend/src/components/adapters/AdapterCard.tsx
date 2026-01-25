import { Download, CheckCircle, CloudOff } from "lucide-react";
import { useTranslation } from "react-i18next";
import type { AdapterDTO } from "@isin/model-service-client";

type AdapterCardProps = {
    adapter: AdapterDTO;
    onDownload: (adapterVersion: number) => Promise<void> | void;
    isDownloading?: boolean;
};

export const AdapterCard = ({ adapter, onDownload, isDownloading = false }: AdapterCardProps) => {
    const { t } = useTranslation();
    const { version, available_local } = adapter;

    return (
        <div className="card bg-base-100 shadow">
            <div className="card-body flex items-center justify-between gap-4">
                <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded bg-base-200 flex items-center justify-center font-medium">
                        v{version}
                    </div>
                    <div>
                        <div className="font-medium">v{version}</div>
                        <div className="text-sm text-base-content/60">
                            {available_local ? (
                                <span className="flex items-center gap-1">
                  <CheckCircle size={14} className="text-success" /> {t("adapters.local")}
                </span>
                            ) : (
                                <span className="flex items-center gap-1">
                  <CloudOff size={14} className="text-warning" /> {t("adapters.notLocal")}
                </span>
                            )}
                        </div>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    {available_local ? (
                        <button className="btn btn-ghost btn-sm" disabled>
                            {t("adapters.local")}
                        </button>
                    ) : (
                        <button
                            className="btn btn-primary btn-sm gap-2"
                            onClick={() => onDownload(version)}
                            disabled={isDownloading}
                            aria-label={t("adapters.download")}
                        >
                            <Download size={14} /> {t("adapters.download")}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};
