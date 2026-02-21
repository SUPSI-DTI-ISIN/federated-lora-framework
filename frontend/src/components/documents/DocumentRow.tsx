import { useState } from "react";
import type { DocumentDTO } from "@isin/data-service-client";
import { motion } from "framer-motion";
import {FileText, Trash2, InspectIcon} from "lucide-react";
import { useDeleteDocument } from "../../hooks/data/documents/useDeleteDocument.ts";
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

    const handleDelete = async (documentId: number) => {
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

    const handleNavigateToSections = () => {
        navigate(`/documents/${document.id}/sections`);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ delay: index * 0.05 }}
            className="group flex items-center gap-4 bg-base-100 hover:bg-base-200/50 p-4 rounded-2xl border border-base-content/5 transition-all duration-200"
        >
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary transition-transform group-hover:scale-110">
                <FileText size={24} />
            </div>

            <div className="flex-1 min-w-0">
                <h3 className="text-base font-bold text-base-content truncate group-hover:text-primary transition-colors">
                    {document.title}
                </h3>
                <div className="flex items-center gap-3 mt-0.5">
                    <span className="text-xs font-mono text-base-content/40 bg-base-200 px-1.5 py-0.5 rounded">
                        Number: {document.number.slice(0, 8)}
                    </span>
                </div>
            </div>

            <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity focus-within:opacity-100">
                <button
                    onClick={handleNavigateToSections}
                    disabled={isDeleting}
                    className="btn btn-circle btn-sm btn-ghost text-error hover:bg-error/10"
                    title={t("documents.list.actions.details")}
                >
                    <InspectIcon size={18} />
                </button>

                <button
                    onClick={() => handleDelete(document.id)}
                    disabled={isDeleting}
                    className="btn btn-circle btn-sm btn-ghost text-error hover:bg-error/10"
                    title={t("documents.list.actions.delete")}
                >
                    {isDeleting ? <span className="loading loading-spinner loading-xs" /> : <Trash2 size={18} />}
                </button>
            </div>
        </motion.div>
    );
};