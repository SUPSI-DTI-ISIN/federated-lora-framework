import { useState, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { AnimatePresence } from "framer-motion";
import { SortDesc, SortAsc, Inbox } from "lucide-react";
import { DepartmentAdapterCard } from "./DepartmentAdapterCard.tsx";

type DepartmentAdaptersListProps = {
    adapters: number[];
};

export const DepartmentAdaptersList = ({ adapters }: DepartmentAdaptersListProps) => {
    const { t } = useTranslation();
    const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

    const sortedAdapters = useMemo(() => {
        return [...adapters].sort((a, b) => {
            const vA = a ?? 0;
            const vB = b ?? 0;
            return sortOrder === "desc" ? vB - vA : vA - vB;
        });
    }, [adapters, sortOrder]);

    if (!adapters || adapters.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center p-12 bg-base-200/30 rounded-3xl border border-dashed border-base-content/10">
                <Inbox className="text-base-content/20 mb-4" size={48} />
                <div className="text-xl font-medium text-base-content/50">{t("adapters.list.empty")}</div>
            </div>
        );
    }

    return (
        <div className="w-full space-y-4">
            {/* List Controls Area */}
            <div className="flex justify-between items-center px-4 mb-2">
                <span className="text-sm font-bold uppercase tracking-widest text-base-content/40">
                    {adapters.length} adapters
                </span>
                <button
                    onClick={() => setSortOrder(prev => prev === "asc" ? "desc" : "asc")}
                    className="btn btn-sm btn-ghost gap-2 hover:bg-base-200 text-primary uppercase tracking-tight"
                >
                    {sortOrder === "desc" ? <SortDesc size={18} /> : <SortAsc size={18} />}
                    {sortOrder === "desc" ? "desc" : "asc"}
                </button>
            </div>

            {/* List Items */}
            <div className="flex flex-col gap-3">
                <AnimatePresence mode="popLayout">
                    {sortedAdapters.map((adapter) => (
                        <DepartmentAdapterCard
                            key={String(adapter)}
                            adapter={adapter}
                        />
                    ))}
                </AnimatePresence>
            </div>
        </div>
    );
};