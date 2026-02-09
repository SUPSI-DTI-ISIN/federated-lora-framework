import type {SectionDTO} from "@isin/data-service-client";
import {AnimatePresence, motion} from "framer-motion";
import {ChevronDown, Trash2} from "lucide-react";
import {useDeleteSection} from "../../hooks/data/sections/useDeleteSection.ts";
import {useState} from "react";
import toast from "react-hot-toast";
import {useTranslation} from "react-i18next";

interface SectionRowProps {
    section: SectionDTO;
    documentId: number;
    expanded?: boolean;
    onToggle: () => void;
}

export const SectionRow = ({section, documentId, expanded = false, onToggle}: SectionRowProps) => {
    const {t} = useTranslation();
    const {mutateAsync: deleteSection} = useDeleteSection();
    const [isDeletingSection, setIsDeletingSection] = useState<boolean>(false)

    const handleDeleteSection = async () => {
        if (!window.confirm(t("sections.delete.confirm"))) return;
        setIsDeletingSection(true);
        try {
            await deleteSection({sectionId: section.id, documentId: documentId});
            toast.success(t("sections.delete.success"));
        } catch (e) {
            console.error(e);
            toast.error(t("sections.delete.error.failed"));
        } finally {
            setIsDeletingSection(false);
        }
    }

    return (
        <motion.div initial={{opacity: 0, y: 6}} animate={{opacity: 1, y: 0}} exit={{opacity: 0, y: -6}}
                    className="bg-base-100 rounded-2xl border border-base-content/5 overflow-hidden">
            <div onClick={onToggle}
                 className="flex items-center justify-between gap-4 p-4 cursor-pointer select-none hover:bg-base-200/40 transition-colors"
                 role="button" aria-expanded={expanded}>
                <div className="flex-1 min-w-0">
                    <h4 className="text-base font-semibold text-base-content truncate">{section.title}</h4>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteSection();
                        }}
                        disabled={isDeletingSection}
                        className="btn btn-circle btn-ghost btn-sm text-error hover:bg-error/10"
                        title={t("sections.delete.action")}
                    >
                        {isDeletingSection ? (
                            <span className="loading loading-spinner loading-xs" />
                        ) : (
                            <Trash2 size={16} />
                        )}
                    </button>

                    <div
                        className={`p-2 rounded-full transition-transform ${
                            expanded ? "rotate-180" : ""
                        }`}
                    >
                        <ChevronDown size={18} />
                    </div>
                </div>
            </div>
            <AnimatePresence initial={false}> {expanded && (
                <motion.div key="content" initial={{height: 0, opacity: 0}} animate={{height: "auto", opacity: 1}}
                            exit={{height: 0, opacity: 0}} transition={{duration: 0.18}} className="px-4 pb-4">
                    <div
                        className="prose max-w-none text-sm text-base-content/80 whitespace-pre-wrap">{section.content}</div>
                </motion.div>)}
            </AnimatePresence>
        </motion.div>
    );
};