import {useState, useCallback, type ChangeEvent, type DragEvent} from 'react';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Upload, X, FileText, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import {useUploadDocument} from "../../hooks/documents/useUploadDocument.ts";

interface DocumentUploadProps {
    onClose: () => void;
}

export const DocumentUpload = ({ onClose }: DocumentUploadProps) => {
    const { t } = useTranslation();
    const { mutateAsync: uploadDocument} = useUploadDocument();
    const [isUploading, setIsUploading] = useState(false);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleDragOver = useCallback((e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback((e: DragEvent<HTMLDivElement>) => {
        if (e.dataTransfer === null || e.dataTransfer === undefined)
            return

        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            setSelectedFile(file);
        } else {
            toast.error(t('documents.upload.error.invalidType'));
        }
    }, [t]);

    const handleFileSelect = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setSelectedFile(file);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsUploading(true);
        try {
            await uploadDocument(selectedFile)
            toast.success(t('documents.upload.success'));
            onClose();
        } catch (error) {
            toast.error(t('documents.upload.error.failed'));
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
                onClick={onClose}
                className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            />

            {/* Modal */}
            <motion.div
                initial={{ opacity: 0, scale: 0.9, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9, y: 20 }}
                className="fixed inset-0 z-50 flex items-center justify-center p-4"
            >
                <div className="card bg-base-100 shadow-2xl w-full max-w-2xl">
                    <div className="card-body">
                        {/* Header */}
                        <div className="flex items-center justify-between mb-4">
                            <h2 className="card-title text-2xl">
                                <Upload className="text-primary" size={28} />
                                {t('documents.upload.title')}
                            </h2>
                            <button
                                onClick={onClose}
                                className="btn btn-ghost btn-sm btn-circle"
                            >
                                <X size={20} />
                            </button>
                        </div>

                        {/* Upload Area */}
                        <div
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onDrop={handleDrop}
                            className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
                                isDragging
                                    ? 'border-primary bg-primary/10'
                                    : 'border-base-300 hover:border-primary/50'
                            }`}
                        >
                            {selectedFile ? (
                                <motion.div
                                    initial={{ scale: 0.8, opacity: 0 }}
                                    animate={{ scale: 1, opacity: 1 }}
                                    className="flex items-center justify-center gap-4"
                                >
                                    <div className="p-3 rounded-lg bg-primary/10">
                                        <FileText className="text-primary" size={32} />
                                    </div>
                                    <div className="text-left">
                                        <p className="font-semibold">{selectedFile.name}</p>
                                        <p className="text-sm text-base-content/60">
                                            {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                                        </p>
                                    </div>
                                    <button
                                        onClick={() => setSelectedFile(null)}
                                        className="btn btn-ghost btn-sm btn-circle ml-auto"
                                    >
                                        <X size={16} />
                                    </button>
                                </motion.div>
                            ) : (
                                <>
                                    <Upload className="mx-auto mb-4 text-base-content/40" size={48} />
                                    <p className="text-lg font-semibold mb-2">
                                        {t('documents.upload.dragDrop')}
                                    </p>
                                    <p className="text-sm text-base-content/60 mb-4">
                                        {t('documents.upload.or')}
                                    </p>
                                    <label className="btn btn-primary">
                                        {t('documents.upload.browse')}
                                        <input
                                            type="file"
                                            accept=".pdf"
                                            onChange={handleFileSelect}
                                            className="hidden"
                                        />
                                    </label>
                                </>
                            )}
                        </div>

                        {/* Info Alert */}
                        <div className="alert alert-info mt-4">
                            <AlertCircle size={20} />
                            <span className="text-sm">{t('documents.upload.info')}</span>
                        </div>

                        {/* Actions */}
                        <div className="card-actions justify-end mt-6">
                            <button
                                onClick={onClose}
                                className="btn btn-ghost"
                                disabled={isUploading}
                            >
                                {t('common.cancel')}
                            </button>
                            <button
                                onClick={handleUpload}
                                disabled={!selectedFile || isUploading}
                                className="btn btn-primary gap-2"
                            >
                                {isUploading ? (
                                    <>
                                        <span className="loading loading-spinner loading-sm"></span>
                                        {t('documents.upload.uploading')}
                                    </>
                                ) : (
                                    <>
                                        <Upload size={18} />
                                        {t('documents.upload.confirm')}
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