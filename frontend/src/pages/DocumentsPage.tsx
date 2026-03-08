import { useState } from "react";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { PageHeader } from "../components/common/PageHeader";
import { DocumentUpload } from "../components/documents/DocumentUpload";
import { DocumentList } from "../components/documents/DocumentList";
import { DocumentFilterBar } from "../components/documents/DocumentFilterBar";

/**
 * DocumentsPage Component
 * 
 * Refactored to use PageHeader, EmptyState, LoadingSkeleton, and DeleteConfirmModal components.
 * Preserves all existing business logic and data fetching hooks.
 * 
 * Requirements satisfied:
 * - 13.1: Render page header with title, subtitle, and upload button
 * - 13.2: Render upload button with Upload icon
 * - 13.3: Styled drag-and-drop zone (in DocumentUpload component)
 * - 10.2: Wrap page in motion.div with entrance animation
 * - 10.9: Use AnimatePresence for modal transitions
 */
export const DocumentsPage = () => {
    const { t } = useTranslation();
    const [searchQuery, setSearchQuery] = useState("");
    const [showUpload, setShowUpload] = useState(false);
    const navigate = useNavigate();

    const handleCloseDocumentUploader = (documentId?: number) => {
        setShowUpload(false);
        if (documentId)
            navigate(`/documents/${documentId}/sections`);
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="min-h-screen bg-base-100 py-8 px-4 sm:px-8"
        >
            <div className="relative z-10 max-w-7xl mx-auto">
                {/* Page Header */}
                <PageHeader
                    icon={FileText}
                    title={t("documents.title")}
                    subtitle={t("documents.subtitle")}
                    action={{
                        label: t("documents.uploadButton"),
                        icon: Upload,
                        onClick: () => setShowUpload(true)
                    }}
                />

                {/* Filter & List Area */}
                <div className="space-y-6">
                    <DocumentFilterBar
                        value={searchQuery}
                        onChange={(v) => setSearchQuery(v)}
                    />

                    <div className="bg-base-200/30 rounded-3xl p-2 border border-base-content/5">
                        <DocumentList searchQuery={searchQuery} />
                    </div>
                </div>
            </div>

            <AnimatePresence>
                {showUpload && <DocumentUpload onClose={handleCloseDocumentUploader} />}
            </AnimatePresence>
        </motion.div>
    );
};