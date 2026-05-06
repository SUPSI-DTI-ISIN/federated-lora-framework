import React, {useCallback, useState, type ChangeEvent} from "react";
import {useTranslation} from "react-i18next";
import {motion} from "framer-motion";
import {Upload, X} from "lucide-react";
import toast from "react-hot-toast";
import {useUploadDocument} from "../../hooks/institute/data/documents/useUploadDocument.ts";
import {DragDropZone} from "./DragDropZone";

interface DocumentUploadProps {
    onClose: (documentId?: number) => void;
}

export const DocumentUpload = ({onClose}: DocumentUploadProps) => {
    const {t} = useTranslation();
    const {mutateAsync: uploadDocument} = useUploadDocument();
    const [isExternallyApproved, setIsExternallyApproved] = useState<boolean>(false);
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
            setIsExternallyApproved(false);
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
        setIsExternallyApproved(false);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;
        setIsUploading(true);
        try {
            const uploadedDocument = await uploadDocument({
                isExternallyApproved,
                file: selectedFile,
            });
            toast.success(t("documents.upload.success"));
            onClose(uploadedDocument.id);
        } catch (e) {
            console.error(e);
            toast.error(t("documents.upload.error.failed"));
        } finally {
            setIsUploading(false);
        }
    };

    const handleClose = () => {
        setSelectedFile(null);
        setIsExternallyApproved(false);
        onClose();
    };

    return (
        <>
            <motion.div
                initial={{opacity: 0}}
                animate={{opacity: 1}}
                exit={{opacity: 0}}
                className="fixed inset-0 bg-base-300/60 backdrop-blur-md z-40"
                onClick={() => !isUploading && onClose()}
            />

            <motion.div
                initial={{opacity: 0, scale: 0.95, y: 20}}
                animate={{opacity: 1, scale: 1, y: 0}}
                exit={{opacity: 0, scale: 0.95, y: 20}}
                className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none"
            >
                <div
                    className="card bg-base-100 shadow-2xl w-full max-w-xl pointer-events-auto border border-base-content/10 overflow-hidden">
                    <div className="p-8">
                        <div className="flex items-center justify-between mb-8">
                            <h3 className="text-2xl font-bold text-base-content flex items-center gap-3">
                                <Upload className="text-primary"/>
                                {t("documents.upload.title")}
                            </h3>
                            <button onClick={handleClose} className="btn btn-ghost btn-sm btn-circle">
                                <X size={20}/>
                            </button>
                        </div>

                        <DragDropZone
                            isDragging={isDragging}
                            selectedFile={selectedFile}
                            onDragOver={onDragOver}
                            onDragLeave={onDragLeave}
                            onDrop={onDrop}
                            onFileSelect={onFileSelect}
                            onRemoveFile={() => setSelectedFile(null)}
                        />

                        {selectedFile && (
                            <motion.div
                                initial={{opacity: 0, y: 10}}
                                animate={{opacity: 1, y: 0}}
                                exit={{opacity: 0, y: 10}}
                                className="mt-6"
                            >
                                <div
                                    className={`rounded-2xl border p-5 transition-all ${
                                        isExternallyApproved
                                            ? "border-success/30 bg-success/10"
                                            : "border-base-content/10 bg-base-200/40"
                                    }`}
                                >
                                    {/* Header */}
                                    <div className="flex items-start justify-between">
                                        <div className="flex flex-col gap-1">
                    <span className="text-sm font-semibold text-base-content">
                        {t("documents.upload.externallyApproved")}
                    </span>
                                            <span className="text-xs text-base-content/60">
                        {t("documents.upload.externallyApprovedHint")}
                    </span>
                                        </div>

                                        <input
                                            type="checkbox"
                                            className="toggle toggle-primary mt-1"
                                            checked={isExternallyApproved}
                                            onChange={(e) => setIsExternallyApproved(e.target.checked)}
                                            disabled={isUploading}
                                        />
                                    </div>

                                    {/* Divider */}
                                    <div className="my-4 h-px bg-base-content/10"/>

                                    {/* Status */}
                                    <div className="flex items-center justify-center">

                                        <span
                                            className={`text-xs font-semibold px-2 py-1 rounded-full ${
                                                isExternallyApproved
                                                    ? "bg-success/20 text-success"
                                                    : "bg-base-300 text-base-content/50"
                                            }`}
                                        >
                    {isExternallyApproved
                        ? t("documents.upload.externallyApprovedYes")
                        : t("documents.upload.externallyApprovedNo")}
                </span>
                                    </div>
                                </div>
                            </motion.div>
                        )}

                        <div className="flex gap-3 mt-8">
                            <button onClick={() => onClose()} className="btn flex-1 bg-base-200 border-none"
                                    disabled={isUploading}>
                                {t("common.cancel")}
                            </button>
                            <button
                                onClick={handleUpload}
                                disabled={!selectedFile || isUploading}
                                className="btn btn-primary flex-2 gap-2 shadow-lg shadow-primary/20"
                            >
                                {isUploading ? <span className="loading loading-spinner loading-sm"/> :
                                    <Upload size={18}/>}
                                {isUploading ? t("documents.upload.uploading") : t("documents.upload.confirm")}
                            </button>
                        </div>
                    </div>
                </div>
            </motion.div>
        </>
    );
};