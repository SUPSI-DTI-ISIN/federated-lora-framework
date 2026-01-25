import { useState } from "react";
import type { DocumentDTO } from "@isin/data-service-client";
import { motion } from "framer-motion";
import { FileText, FileIcon, Trash2 } from "lucide-react";
import { useDeleteDocument } from "../../hooks/documents/useDeleteDocument";
import { useTranslation } from "react-i18next";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

interface DocumentRowProps {
    document: DocumentDTO;
    index: number;
}

export const DocumentRow = ({ document, index }: DocumentRowProps) => {
    const { t } = useTranslation();
    const { mutateAsync: deleteDocument } = useDeleteDocument();
    const [isDeleting, setIsDeleting] = useState(false);
    const navigate = useNavigate();

    const handleDelete = async (documentId: string) => {
        if (!window.confirm(t("documents.list.deleteConfirm"))) return;

        setIsDeleting(true);
        try {
            await deleteDocument(documentId);
            toast.success(t("documents.list.deleteSuccess"));
            navigate("/documents");
        } catch (e) {
            console.error(e);
            toast.error(t("documents.list.deleteError"));
            setIsDeleting(false);
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -80 }}
            transition={{ delay: index * 0.03 }}
            className="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow"
            role="listitem"
            aria-label={document.title ?? document.id}
        >
            <div className="card-body">
                <div className="flex flex-col md:flex-row md:items-center gap-4">
                    {/* Icon */}
                    <div className="shrink-0">
                        <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                            <FileText className="text-primary" size={22} />
                        </div>
                    </div>

                    {/* Info */}
                    <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-lg truncate mb-1">{document.title ?? document.id}</h3>
                        <div className="flex flex-wrap items-center gap-3 text-sm text-base-content/60">
              <span className="flex items-center gap-1">
                <FileIcon size={14} />
                  {document.id}
              </span>
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                        <button
                            onClick={() => handleDelete(document.id)}
                            disabled={isDeleting}
                            className="btn btn-ghost btn-sm text-error gap-2"
                            title={t("documents.list.actions.delete")}
                            aria-label={t("documents.list.actions.delete") as string}
                        >
                            {isDeleting ? (
                                <span className="loading loading-spinner loading-xs" aria-hidden />
                            ) : (
                                <Trash2 size={16} />
                            )}
                            <span className="hidden md:inline">{t("documents.list.actions.delete")}</span>
                        </button>
                    </div>
                </div>
            </div>
        </motion.div>
    );
};