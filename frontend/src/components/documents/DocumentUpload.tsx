import React, { useCallback, useState, type ChangeEvent } from "react";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { Upload, X, FileText, CloudUpload } from "lucide-react";
import toast from "react-hot-toast";
import { useUploadDocument } from "../../hooks/institute/data/documents/useUploadDocument.ts";

interface DocumentUploadProps {
    onClose: (documentId?: number) => void;
}

/**
 * DocumentUpload Component
 * 
 * Modal for uploading PDF documents with drag-and-drop support.
 * Preserves all existing business logic and upload handlers.
 * 
 * Requirements satisfied:
 * - 13.3: Create drag-and-drop zone with dashed indigo border and cloud upload icon
 * - 13.4: Display translated hint text in upload zone
 * - 13.13: Preserve existing upload handler logic
 */
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
            const uploadedDocument = await uploadDocument(selectedFile);
            toast.success(t("documents.upload.success"));
            onClose(uploadedDocument.id);
        } catch (e) {
            console.error(e);
            toast.error(t("documents.upload.error.failed"));
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 bg-base-300/60 backdrop-blur-md z-40"
                onClick={() => !isUploading && onClose()}
            />

            <motion.div
                initial={{ opacity: 0, scale: 0.95, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95, y: 20 }}
                className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none"
            >
                <div className="card bg-base-100 shadow-2xl w-full max-w-xl pointer-events-auto border border-base-content/10 overflow-hidden">
                    <div className="p-8">
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="text-2xl font-bold text-base-content flex items-center gap-3">
                                <Upload className="text-primary" />
                                {t("documents.upload.title")}
                            </h3>
                            <button onClick={() => onClose()} className="btn btn-ghost btn-sm btn-circle"><X size={20} /></button>
                        </div>

                        {/* Drag-and-drop zone with dashed indigo border */}
                        <div
                            onDragOver={onDragOver}
                            onDragLeave={onDragLeave}
                            onDrop={onDrop}
                            className={`relative border-3 border-dashed rounded-2xl p-10 transition-all duration-300 flex flex-col items-center justify-center ${
                                isDragging
                                    ? "border-indigo-500 bg-indigo-500/5 scale-[1.02]"
                                    : "border-indigo-300 dark:border-indigo-700 bg-base-200/30 hover:bg-base-200/50"
                            }`}
                        >
                            {selectedFile ? (
                                <div className="flex items-center gap-5 w-full bg-base-100 p-4 rounded-xl shadow-sm border border-primary/20">
                                    <div className="p-3 bg-primary/10 rounded-lg text-primary">
                                        <FileText size={32} />
                                    </div>
                                    <div className="flex-1 overflow-hidden">
                                        <p className="font-bold truncate text-base-content">{selectedFile.name}</p>
                                        <p className="text-xs font-medium text-base-content/50 uppercase">
                                            {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                                        </p>
                                    </div>
                                    <button onClick={() => setSelectedFile(null)} className="btn btn-circle btn-xs btn-ghost text-error">
                                        <X size={16} />
                                    </button>
                                </div>
                            ) : (
                                <div className="text-center">
                                    {/* Cloud upload icon */}
                                    <div className="mx-auto w-16 h-16 bg-indigo-500/10 rounded-full flex items-center justify-center mb-4">
                                        <CloudUpload className="text-indigo-600 dark:text-indigo-400" size={32} />
                                    </div>
                                    <p className="text-lg font-bold text-base-content">{t("documents.upload.dragDrop")}</p>
                                    <p className="text-sm text-base-content/50 mt-1 mb-6">{t("documents.upload.info")}</p>
                                    <label className="btn btn-sm btn-outline px-6">
                                        {t("documents.upload.browse")}
                                        <input type="file" accept="application/pdf" className="hidden" onChange={onFileSelect} />
                                    </label>
                                </div>
                            )}
                        </div>

                        <div className="flex gap-3 mt-8">
                            <button onClick={() => onClose()} className="btn flex-1 bg-base-200 border-none" disabled={isUploading}>
                                {t("common.cancel")}
                            </button>
                            <button
                                onClick={handleUpload}
                                disabled={!selectedFile || isUploading}
                                className="btn btn-primary flex-2 gap-2 shadow-lg shadow-primary/20"
                            >
                                {isUploading ? <span className="loading loading-spinner loading-sm" /> : <Upload size={18} />}
                                {isUploading ? t("documents.upload.uploading") : t("documents.upload.confirm")}
                            </button>
                        </div>
                    </div>
                </div>
            </motion.div>
        </>
    );
};