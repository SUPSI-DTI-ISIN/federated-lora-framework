import { useParams } from "react-router-dom";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useGetDocumentById } from "../hooks/institute/data/documents/useGetDocumentById.ts";
import { SectionsHeader } from "../components/sections/SectionsHeader";
import { SectionsList } from "../components/sections/SectionsList";
import { useDeleteSection } from "../hooks/institute/data/sections/useDeleteSection.ts";
import toast from "react-hot-toast";
import { Trash2 } from "lucide-react";
import { DeleteConfirmModal } from "../components/common/DeleteConfirmModal.tsx";


export const SectionsPage = () => {
    const { t } = useTranslation();
    const { documentId } = useParams();
    const {
        data: document,
        isLoading: isLoadingDocument,
        error: errorLoadingDocument,
    } = useGetDocumentById(Number(documentId!));

    const { mutateAsync: deleteSection } = useDeleteSection();
    const [selectedSections, setSelectedSections] = useState<number[]>([]);
    const [isDeleting, setIsDeleting] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);

    const handleSelectAll = () => {
        if (!document?.sections) return;
        if (selectedSections.length === document.sections.length) {
            setSelectedSections([]);
        } else {
            setSelectedSections(document.sections.map(s => s.id));
        }
    };

    const handleSelectSection = (sectionId: number) => {
        setSelectedSections(prev =>
            prev.includes(sectionId)
                ? prev.filter(id => id !== sectionId)
                : [...prev, sectionId]
        );
    };

    const handleBulkDelete = async () => {
        setShowDeleteModal(false);
        setIsDeleting(true);
        
        let successCount = 0;
        let errorCount = 0;

        for (const sectionId of selectedSections) {
            try {
                await deleteSection({ sectionId, documentId: Number(documentId!) });
                successCount++;
            } catch (e) {
                console.error(e);
                errorCount++;
            }
        }

        setIsDeleting(false);
        setSelectedSections([]);

        if (errorCount === 0) {
            toast.success(t("sections.delete.bulkSuccess", { count: successCount }));
        } else if (successCount === 0) {
            toast.error(t("sections.delete.bulkError"));
        } else {
            toast.success(t("sections.delete.bulkPartial", { success: successCount, failed: errorCount }));
        }
    };


    if (isLoadingDocument) {
        return (
            <div className="min-h-screen bg-base-100 py-8 px-4 sm:px-8">
                <div className="max-w-7xl mx-auto">
                    <div className="card bg-base-100 shadow-lg p-8">
                        <div className="h-8 bg-base-200 rounded w-1/3 animate-pulse" />
                        <div className="mt-6 space-y-3">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="h-16 bg-base-200 rounded animate-pulse" />
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        );
    }


    if (errorLoadingDocument || !document) {
        return (
            <div className="min-h-screen bg-base-100 py-8 px-4 sm:px-8">
                <div className="max-w-7xl mx-auto">
                    <div className="card bg-base-100 shadow-lg p-8 text-center">
                        <h3 className="text-xl font-semibold">{t("sections.error.title")}</h3>
                        <p className="text-base-content/60">{t("sections.error.description")}</p>
                    </div>
                </div>
            </div>
        );
    }


    return (
        <>
            <div className="min-h-screen bg-base-100 py-8 px-4 sm:px-8">
                <div className="max-w-7xl mx-auto">
                    <SectionsHeader title={document.title} number={document.number} />

                    {/* Selection Controls */}
                    {document.sections && document.sections.length > 0 && (
                        <div className="flex items-center justify-between mb-4 p-4 bg-base-200/50 rounded-xl border border-base-content/5">
                            <label className="flex items-center gap-3 cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={selectedSections.length === document.sections.length && document.sections.length > 0}
                                    onChange={handleSelectAll}
                                    className="checkbox checkbox-primary"
                                />
                                <span className="font-medium">
                                    {selectedSections.length === document.sections.length && document.sections.length > 0
                                        ? t("sections.selection.deselectAll")
                                        : t("sections.selection.selectAll")}
                                </span>
                            </label>

                            {selectedSections.length > 0 && (
                                <button
                                    onClick={() => setShowDeleteModal(true)}
                                    disabled={isDeleting}
                                    className="btn btn-error gap-2"
                                >
                                    {isDeleting ? (
                                        <span className="loading loading-spinner loading-sm" />
                                    ) : (
                                        <Trash2 size={18} />
                                    )}
                                    <span>{t("sections.selection.deleteSelected", { count: selectedSections.length })}</span>
                                </button>
                            )}
                        </div>
                    )}

                    <div className="mt-6 bg-base-200/30 rounded-3xl p-4 border border-base-content/5">
                        <SectionsList
                            documentId={document.id}
                            sections={document.sections}
                            selectedSections={selectedSections}
                            onSelectSection={handleSelectSection}
                        />
                    </div>
                </div>
            </div>

            <DeleteConfirmModal
                isOpen={showDeleteModal}
                onConfirm={handleBulkDelete}
                onCancel={() => setShowDeleteModal(false)}
                itemName={t("sections.selection.deleteConfirm", { count: selectedSections.length })}
            />
        </>
    );
};
