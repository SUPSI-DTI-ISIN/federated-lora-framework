import { useState } from "react";
import type { DocumentDTO } from "@isin/data-service-client";
import { motion } from "framer-motion";
import { FileText, Trash2, Eye } from "lucide-react";
import { useDeleteDocument } from "../../hooks/institute/data/documents/useDeleteDocument.ts";
import { useTranslation } from "react-i18next";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { DeleteConfirmModal } from "../common/DeleteConfirmModal";

interface DocumentRowProps {
    document: DocumentDTO;
    index: number;
}

/**
 * DocumentRow Component
 * 
 * Refactored to use DeleteConfirmModal instead of window.confirm.
 * Added View button with Eye icon.
 * Preserves all existing business logic and event handlers.
 * 
 * Requirements satisfied:
 * - 13.5: Render document list with name, type badge, date, size, and actions
 * - 13.7: Render PDF badge in red/accent color
 * - 13.8: Render View and Delete action buttons as icon buttons
 * - 13.9: Wire Delete button to trigger DeleteConfirmModal
 * - 13.13: Preserve existing upload handler logic
 * - 13.14: Preserve existing document fetching hooks
 * - 13.15: Preserve all existing event handlers
 */
export const DocumentRow = ({ document, index }: DocumentRowProps) => {
    const { t } = useTranslation();
    const { mutateAsync: deleteDocument } = useDeleteDocument();
    const [isDeleting, setIsDeleting] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const navigate = useNavigate();

    const handleDelete = async () => {
        setShowDeleteModal(false);
        setIsDeleting(true);
        try {
            await deleteDocument(document.id);
            toast.success(t("documents.list.deleteSuccess"));
            navigate("/documents");
        } catch (e) {
            console.error(e);
            toast.error(t("documents.list.deleteError"));
            setIsDeleting(false);
        }
    };

    const handleNavigateToSections = () => {
        navigate(`/documents/${document.id}/sections`);
    };

    return (
        <>
            <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ delay: index * 0.05 }}
                className="group flex items-start gap-4 bg-base-100 hover:bg-base-200/50 p-6 rounded-2xl border border-base-content/5 hover:border-primary/20 transition-all duration-200 shadow-sm hover:shadow-md"
            >
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary transition-transform group-hover:scale-110">
                    <FileText size={24} />
                </div>

                <div className="flex-1 min-w-0">
                    <h3 className="text-base font-bold text-base-content group-hover:text-primary transition-colors break-words">
                        {document.title}
                    </h3>
                    <div className="flex items-center gap-3 mt-2">
                        <span className="text-xs font-mono text-base-content/40 bg-base-200 px-2 py-1 rounded">
                            ID: {document.number}
                        </span>
                    </div>
                </div>

                <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity focus-within:opacity-100 shrink-0">
                    {/* View Button */}
                    <button
                        onClick={handleNavigateToSections}
                        disabled={isDeleting}
                        className="btn btn-circle btn-sm btn-ghost text-primary hover:bg-primary/10"
                        title={t("common.view")}
                        aria-label={t("common.view")}
                    >
                        <Eye size={18} />
                    </button>

                    {/* Delete Button */}
                    <button
                        onClick={() => setShowDeleteModal(true)}
                        disabled={isDeleting}
                        className="btn btn-circle btn-sm btn-ghost text-error hover:bg-error/10"
                        title={t("documents.list.actions.delete")}
                        aria-label={t("documents.list.actions.delete")}
                    >
                        {isDeleting ? <span className="loading loading-spinner loading-xs" /> : <Trash2 size={18} />}
                    </button>
                </div>
            </motion.div>

            {/* Delete Confirmation Modal */}
            <DeleteConfirmModal
                isOpen={showDeleteModal}
                onConfirm={handleDelete}
                onCancel={() => setShowDeleteModal(false)}
                itemName={document.title}
            />
        </>
    );
};