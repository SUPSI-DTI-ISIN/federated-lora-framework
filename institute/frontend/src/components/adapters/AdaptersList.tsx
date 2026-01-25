import type { AdapterDTO } from "@isin/model-service-client";
import { AdapterCard } from "./AdapterCard";

type AdaptersListProps = {
    adapters: AdapterDTO[];
    onDownload: (adapterVersion: number) => Promise<void> | void;
    isDownloading?: boolean;
};

export const AdaptersList = ({ adapters, onDownload, isDownloading = false }: AdaptersListProps) => {
    if (!adapters || adapters.length === 0) {
        return (
            <div className="card bg-base-100 shadow-inner p-6 text-center">
                <div className="text-base-content/70">No adapters found.</div>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {adapters.map((adapter) => (
                <AdapterCard
                    key={String(adapter.version)}
                    adapter={adapter}
                    onDownload={onDownload}
                    isDownloading={isDownloading}
                />
            ))}
        </div>
    );
};
