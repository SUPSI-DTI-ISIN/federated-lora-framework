import type {SectionDTO} from "@isin/data-service-client";
import {AnimatePresence, motion} from "framer-motion";
import {ChevronDown, Pencil, X} from "lucide-react";
import {useState} from "react";
import toast from "react-hot-toast";
import {useTranslation} from "react-i18next";
import {useUpdateSectionContent} from "../../hooks/institute/data/sections/useUpdateSectionContent.ts";

interface SectionRowProps {
    section: SectionDTO;
    documentId: number;
    expanded?: boolean;
    onToggle: () => void;
    isSelected?: boolean;
    onSelect?: () => void;
}

export const SectionRow = ({
                               section,
                               documentId,
                               expanded = false,
                               onToggle,
                               isSelected = false,
                               onSelect
                           }: SectionRowProps) => {
    const {t} = useTranslation();
    const {mutateAsync: updateSection} = useUpdateSectionContent();
    const [isUpdating, setIsUpdating] = useState<boolean>(false);
    const [isEditing, setIsEditing] = useState<boolean>(false);
    const [editedContent, setEditedContent] = useState<string>(section.content ?? "");

    const handleStartEditing = () => {
        setEditedContent(section.content ?? "");
        setIsEditing(true);
    };

    const handleCancelEditing = () => {
        setEditedContent(section.content ?? "");
        setIsEditing(false);
    };

    const handleUpdateSection = async () => {
        setIsUpdating(true);
        try {
            await updateSection({sectionId: section.id, documentId, updatedContent: editedContent});
            toast.success(t("sections.update.success"));
            setIsEditing(false);
        } catch (e) {
            console.error(e);
            toast.error(t("sections.update.error.failed"));
        } finally {
            setIsUpdating(false);
        }
    };

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
                        <div className="flex-1 min-w-0 cursor-pointer select-none" onClick={onToggle} role="button"
                             aria-expanded={expanded}>
                            <h4 className="text-base font-semibold text-base-content truncate">{section.title}</h4>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <div
                            onClick={onToggle}
                            className={`p-2 rounded-full transition-transform cursor-pointer ${
                                expanded ? "rotate-180" : ""
                            }`}
                        >
                            <ChevronDown size={18}/>
                        </div>
                    </div>
                </div>
                <AnimatePresence initial={false}> {expanded && (
                    <motion.div key="content" initial={{height: 0, opacity: 0}} animate={{height: "auto", opacity: 1}}
                                exit={{height: 0, opacity: 0}} transition={{duration: 0.18}} className="px-4 pb-4">
                        {isEditing ? (
                            <>
                                <textarea
                                    className="textarea textarea-bordered w-full text-sm text-base-content/80 resize-y min-h-[120px] font-mono leading-relaxed"
                                    value={editedContent}
                                    onChange={(e) => setEditedContent(e.target.value)}
                                    disabled={isUpdating}
                                    aria-label={t("sections.update.editLabel")}
                                    autoFocus
                                />
                                <div className="flex justify-end gap-2 mt-2">
                                    <button
                                        className="btn btn-ghost btn-sm gap-1"
                                        onClick={handleCancelEditing}
                                        disabled={isUpdating}
                                    >
                                        <X size={14}/>
                                        {t("sections.update.cancel")}
                                    </button>
                                    <button
                                        className="btn btn-primary btn-sm gap-1"
                                        onClick={handleUpdateSection}
                                        disabled={isUpdating}
                                    >
                                        {isUpdating ? <span className="loading loading-spinner loading-xs"/> : null}
                                        {t("sections.update.save")}
                                    </button>
                                </div>
                            </>
                        ) : (
                            <>
                                <div className="prose max-w-none text-sm text-base-content/80 whitespace-pre-wrap">
                                    {section.content}
                                </div>
                                <div className="flex justify-end mt-2">
                                    <button
                                        className="btn btn-ghost btn-sm gap-1 text-base-content/60 hover:text-base-content"
                                        onClick={handleStartEditing}
                                    >
                                        <Pencil size={14}/>
                                        {t("sections.update.edit")}
                                    </button>
                                </div>
                            </>
                        )}
                    </motion.div>)}
                </AnimatePresence>
            </motion.div>
        </>
    );
};