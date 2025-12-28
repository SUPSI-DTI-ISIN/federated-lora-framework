import type {DocumentDTO} from "@isin/data-service-client";
import { motion } from "framer-motion";
import {FileIcon, FileText, Trash2} from "lucide-react";
import {useDeleteDocument} from "../../hooks/documents/useDeleteDocument.ts";
import {useTranslation} from "react-i18next";
import toast from "react-hot-toast";
import {useState} from "react";
import {useNavigate} from "react-router-dom";

interface DocumentRowProps {
    document: DocumentDTO;
    index: number;
}

export const DocumentRow = ({document, index}: DocumentRowProps) => {
    const { t } = useTranslation();
    const { mutateAsync: deleteDocument} = useDeleteDocument();
    const [isDeletingDocument, setIsDeletingDocument] = useState<boolean>(false);
    const navigate = useNavigate()

    const handleDelete = async (id: string) => {
        if (!window.confirm(t('documents.list.deleteConfirm'))) return;

        setIsDeletingDocument(true)
        try {
            await deleteDocument(id);
            navigate("/documents")
            toast.success(t('documents.list.deleteSuccess'));
        } catch (error) {
            toast.error(t('documents.list.deleteError'));
            setIsDeletingDocument(false)
        }
    };

    return (
        <motion.div
            key={document.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ delay: index * 0.05 }}
            className="card bg-base-100 shadow-lg hover:shadow-xl transition-shadow"
        >
            <div className="card-body">
                <div className="flex flex-col md:flex-row md:items-center gap-4">
                    {/* Icon */}
                    <div className="shrink-0">
                        <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                            <FileText className="text-primary" size={24} />
                        </div>
                    </div>

                    {/* Info */}
                    <div className="flex-1 min-w-0">
                        <h3 className="font-semibold text-lg truncate mb-1">
                            {document.id}
                        </h3>
                        <div className="flex flex-wrap items-center gap-3 text-sm text-base-content/60">
                            <span className="flex items-center gap-1">
                                <FileIcon size={14} />
                                {document.title}
                            </span>
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-2">
                        <button
                            onClick={() => handleDelete(document.id)}
                            disabled={isDeletingDocument}
                            className="btn btn-ghost btn-sm text-error gap-2"
                            title={t('documents.list.actions.delete')}
                        >
                            {isDeletingDocument ? (
                                <span className="loading loading-spinner loading-xs"></span>
                            ) : (
                                <Trash2 size={18} />
                            )}
                        </button>
                    </div>
                </div>
            </div>
        </motion.div>
    )
}