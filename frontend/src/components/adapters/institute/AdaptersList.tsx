import { useState, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { AnimatePresence, motion } from "framer-motion";
import { SortDesc, SortAsc, Inbox } from "lucide-react";
import type { AdapterDTO } from "@isin/model-service-client";
import { AdapterCard } from "./AdapterCard.tsx";
import { useReducedMotion } from "../../../hooks/useReducedMotion";

interface AdaptersListProps {
    adapters: AdapterDTO[];
    modelKey: string;
}

export const AdaptersList = ({ adapters, modelKey }: AdaptersListProps) => {
    const { t } = useTranslation();
    const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
    const prefersReducedMotion = useReducedMotion();

    const sortedAdapters = useMemo(() => {
        return [...adapters].sort((a, b) => {
            const vA = a.version ?? 0;
            const vB = b.version ?? 0;
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
                    aria-label={`Sort adapters ${sortOrder === "desc" ? "ascending" : "descending"}`}
                >
                    {sortOrder === "desc" ? <SortDesc size={18} aria-hidden="true" /> : <SortAsc size={18} aria-hidden="true" />}
                    {sortOrder === "desc" ? "desc" : "asc"}
                </button>
            </div>

            {/* List Items */}
            <motion.div
                initial="hidden"
                animate="visible"
                variants={prefersReducedMotion ? {} : {
                    visible: {
                        transition: {
                            staggerChildren: 0.05
                        }
                    }
                }}
                className="flex flex-col gap-3"
            >
                <AnimatePresence mode="popLayout">
                    {sortedAdapters.map((adapter) => (
                        <motion.div
                            key={String(adapter.version)}
                            variants={prefersReducedMotion ? {} : {
                                hidden: { opacity: 0, y: 8 },
                                visible: { opacity: 1, y: 0 }
                            }}
                        >
                            <AdapterCard
                                adapter={adapter}
                                modelKey={modelKey}
                            />
                        </motion.div>
                    ))}
                </AnimatePresence>
            </motion.div>
        </div>
    );
};