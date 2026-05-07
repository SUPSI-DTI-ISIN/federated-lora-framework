import { useState } from "react";
import type { SectionDTO } from "@isin/data-service-client";
import { SectionRow } from "./SectionRow";
import { useTranslation } from "react-i18next";
import { ChevronDown, ChevronUp, LayoutList } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";

interface SectionsListProps {
    documentId: number;
    sections: Array<SectionDTO>;
    selectedSections?: number[];
    onSelectSection?: (sectionId: number) => void;
}

export const SectionsList = ({ documentId, sections, selectedSections = [], onSelectSection }: SectionsListProps) => {
    const { t } = useTranslation();
    const [isOpen, setIsOpen] = useState(false);
    const [expandedIds, setExpandedIds] = useState<Array<number>>([]);

    const toggle = (id: number) => {
        setExpandedIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
    };

    const isEmpty = !sections || sections.length === 0;

    return (
        <div className="bg-base-100 rounded-2xl border border-base-content/5 shadow-sm overflow-hidden">
            <button
                onClick={() => setIsOpen((prev) => !prev)}
                disabled={isEmpty}
                className="w-full flex items-center justify-between px-6 py-4 hover:bg-base-200/50 transition-colors cursor-pointer disabled:cursor-default disabled:opacity-60"
            >
                <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                        <LayoutList size={20} />
                    </div>

                    <div className="flex flex-col items-start">
                        <span className="font-bold text-base-content">
                            {t("sections.list.title")}
                        </span>
                        <span className="text-xs text-base-content/50">
                            {isEmpty
                                ? t("sections.empty")
                                : t("sections.list.subtitle", { count: sections.length })}
                        </span>
                    </div>
                </div>

                {!isEmpty && (
                    isOpen
                        ? <ChevronUp size={18} className="text-base-content/40" />
                        : <ChevronDown size={18} className="text-base-content/40" />
                )}
            </button>

            <AnimatePresence initial={false}>
                {isOpen && !isEmpty && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.2 }}
                        className="overflow-hidden"
                    >
                        <div className="px-6 pb-6 pt-2 space-y-3">
                            {sections.map((section) => (
                                <SectionRow
                                    key={section.id}
                                    section={section}
                                    documentId={documentId}
                                    expanded={expandedIds.includes(section.id)}
                                    onToggle={() => toggle(section.id)}
                                    isSelected={selectedSections.includes(section.id)}
                                    onSelect={onSelectSection ? () => onSelectSection(section.id) : undefined}
                                />
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};