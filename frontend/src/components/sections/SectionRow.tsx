import type {SectionDTO} from "@isin/data-service-client";
import {AnimatePresence, motion} from "framer-motion";
import {ChevronDown, Trash2} from "lucide-react";
import {useDeleteSection} from "../../hooks/institute/data/sections/useDeleteSection.ts";
import {useState} from "react";
import toast from "react-hot-toast";
import {useTranslation} from "react-i18next";
import {DeleteConfirmModal} from "../common/DeleteConfirmModal.tsx";

interface SectionRowProps {
    section: SectionDTO;
    documentId: number;
    expanded?: boolean;
    onToggle: () => void;
    isSelected?: boolean;
    onSelect?: () => void;
}

export const SectionRow = ({section, documentId, expanded = false, onToggle, isSelected = false, onSelect}: SectionRowProps) => {
    const {t} = useTranslation();
    const {mutateAsync: deleteSection} = useDeleteSection();
    const [isDeletingSection, setIsDeletingSection] = useState<boolean>(false);
    const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);

    const handleDeleteSection = async () => {
        setShowDeleteModal(false);
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
        <>
            <motion.div initial={{opacity: 0, y: 6}} animate={{opacity: 1, y: 0}} exit={{opacity: 0, y: -6}}
                        className={`bg-base-100 rounded-2xl border transition-all ${isSelected ? 'border-primary ring-2 ring-primary/20' : 'border-base-content/5'} overflow-hidden`}>
                <div
                     className="flex items-center justify-between gap-4 p-4 hover:bg-base-200/40 transition-colors">
                    <div className="flex items-center gap-4 flex-1 min-w-0">
                        {onSelect && (
                            <input
                                type="checkbox"
                                checked={isSelected}
                                onChange={(e) => {
                                    e.stopPropagation();
                                    onSelect();
                                }}
                                className="checkbox checkbox-primary"
                                onClick={(e) => e.stopPropagation()}
                            />
                        )}
                        <div className="flex-1 min-w-0 cursor-pointer select-none" onClick={onToggle} role="button" aria-expanded={expanded}>
                            <h4 className="text-base font-semibold text-base-content truncate">{section.title}</h4>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        {!onSelect && (
                            <button
                                onClick={(e) => {
                                    e.stopPropagation();
                                    setShowDeleteModal(true);
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
                        )}

                        <div
                            onClick={onToggle}
                            className={`p-2 rounded-full transition-transform cursor-pointer ${
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

            {!onSelect && (
                <DeleteConfirmModal
                    isOpen={showDeleteModal}
                    onConfirm={handleDeleteSection}
                    onCancel={() => setShowDeleteModal(false)}
                    itemName={section.title}
                />
            )}
        </>
    );
};