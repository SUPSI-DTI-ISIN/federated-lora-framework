import React from "react";
import {useTranslation} from "react-i18next";
import {FileText, CloudUpload, X} from "lucide-react";

interface DragDropZoneProps {
    isDragging: boolean;
    selectedFile: File | null;
    onDragOver: (e: React.DragEvent) => void;
    onDragLeave: (e: React.DragEvent) => void;
    onDrop: (e: React.DragEvent) => void;
    onFileSelect: (e: React.ChangeEvent<HTMLInputElement>) => void;
    onRemoveFile: () => void;
}

export const DragDropZone = ({
                                 isDragging,
                                 selectedFile,
                                 onDragOver,
                                 onDragLeave,
                                 onDrop,
                                 onFileSelect,
                                 onRemoveFile,
                             }: DragDropZoneProps) => {
    const {t} = useTranslation();

    return (
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
                <div
                    className="flex items-center gap-5 w-full bg-base-100 p-4 rounded-xl shadow-sm border border-primary/20">
                    <div className="p-3 bg-primary/10 rounded-lg text-primary">
                        <FileText size={32}/>
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <p className="font-bold truncate text-base-content">{selectedFile.name}</p>
                        <p className="text-xs font-medium text-base-content/50 uppercase">
                            {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
                        </p>
                    </div>
                    <button onClick={onRemoveFile} className="btn btn-circle btn-xs btn-ghost text-error">
                        <X size={16}/>
                    </button>
                </div>
            ) : (
                <div className="text-center">
                    <div
                        className="mx-auto w-16 h-16 bg-indigo-500/10 rounded-full flex items-center justify-center mb-4">
                        <CloudUpload className="text-indigo-600 dark:text-indigo-400" size={32}/>
                    </div>
                    <p className="text-lg font-bold text-base-content">{t("documents.upload.dragDrop")}</p>
                    <p className="text-sm text-base-content/50 mt-1 mb-6">{t("documents.upload.info")}</p>
                    <label className="btn btn-sm btn-outline px-6">
                        {t("documents.upload.browse")}
                        <input type="file" accept="application/pdf" className="hidden" onChange={onFileSelect}/>
                    </label>
                </div>
            )}
        </div>
    );
}
