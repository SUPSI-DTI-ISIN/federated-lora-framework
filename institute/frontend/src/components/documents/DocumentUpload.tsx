import React, { useCallback, useState, type ChangeEvent } from "react";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { Upload, X, FileText, AlertCircle } from "lucide-react";
import toast from "react-hot-toast";
import { useUploadDocument } from "../../hooks/documents/useUploadDocument";

interface DocumentUploadProps {
    onClose: () => void;
}

export const DocumentUpload = ({ onClose }: DocumentUploadProps) => {
    const { t } = useTranslation();
    const { mutateAsync: uploadDocument } = useUploadDocument();
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);

    const onDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const onDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const onDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault();
            setIsDragging(false);
            const file = e.dataTransfer?.files?.[0];
            if (!file) return;
            if (file.type !== "application/pdf") {
                toast.error(t("documents.upload.error.invalidType"));
                return;
            }
            setSelectedFile(file);
        },
        [t]
    );

    const onFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        if (file.type !== "application/pdf") {
            toast.error(t("documents.upload.error.invalidType"));
            return;
        }
        setSelectedFile(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;
        setIsUploading(true);
        try {
            await uploadDocument(selectedFile);
            toast.success(t("documents.upload.success"));
            onClose();
        } catch (e) {
            console.error(e);
            toast.error(t("documents.upload.error.failed"));
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <>
            {/* Backdrop */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={() => !isUploading && onClose()}
                className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
                role="presentation"
            />

            {/* Modal */}
            <motion.div
                initial={{ opacity: 0, scale: 0.98, y: 8 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.98, y: 8 }}
                className="fixed inset-0 z-50 flex items-center justify-center p-4"
                aria-modal="true"
                role="dialog"
            >
                <div className="card bg-base-100 shadow-2xl w-full max-w-2xl">
                    <div className="card-body">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="card-title text-2xl flex items-center gap-3">
                                <Upload className="text-primary" size={28} />
                                {t("documents.upload.title")}
                            </h3>
                            <button
                                onClick={() => !isUploading && onClose()}
                                className="btn btn-ghost btn-sm btn-circle"
                                aria-label={t("common.close")}
                            >
                                <X size={18} />
                            </button>
                        </div>

                        <div
                            onDragOver={onDragOver}
                            onDragLeave={onDragLeave}
                            onDrop={onDrop}
                            className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
                                isDragging ? "border-primary bg-primary/10" : "border-base-300 hover:border-primary/50"
                            }`}
                        >
                            {selectedFile ? (
                                <motion.div initial={{ opacity: 0.9 }} animate={{ opacity: 1 }}>
                                    <div className="flex items-center gap-4">
                                        <div className="p-3 rounded-lg bg-primary/10">
                                            <FileText className="text-primary" size={32} />
                                        </div>
                                        <div className="text-left">
                                            <p className="font-semibold">{selectedFile.name}</p>
                                            <p className="text-sm text-base-content/60">
                                                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                                            </p>
                                        </div>
                                        <div className="ml-auto">
                                            <button onClick={() => setSelectedFile(null)} className="btn btn-ghost btn-sm btn-circle" aria-label={t("common.cancel")}>
                                                <X size={16} />
                                            </button>
                                        </div>
                                    </div>
                                </motion.div>
                            ) : (
                                <>
                                    <Upload className="mx-auto mb-4 text-base-content/40" size={48} />
                                    <p className="text-lg font-semibold mb-2">{t("documents.upload.dragDrop")}</p>
                                    <p className="text-sm text-base-content/60 mb-4">{t("documents.upload.or")}</p>
                                    <label className="btn btn-primary">
                                        {t("documents.upload.browse")}
                                        <input type="file" accept="application/pdf" className="hidden" onChange={onFileSelect} />
                                    </label>
                                </>
                            )}
                        </div>

                        <div className="alert alert-info mt-4">
                            <AlertCircle size={20} />
                            <span className="text-sm">{t("documents.upload.info")}</span>
                        </div>

                        <div className="card-actions justify-end mt-6">
                            <button onClick={() => !isUploading && onClose()} className="btn btn-ghost" disabled={isUploading}>
                                {t("common.cancel")}
                            </button>

                            <button onClick={handleUpload} disabled={!selectedFile || isUploading} className="btn btn-primary gap-2">
                                {isUploading ? (
                                    <>
                                        <span className="loading loading-spinner loading-sm" aria-hidden />
                                        {t("documents.upload.uploading")}
                                    </>
                                ) : (
                                    <>
                                        <Upload size={18} />
                                        {t("documents.upload.confirm")}
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </motion.div>
        </>
    );
};