import { useState } from "react";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Upload } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { PageHeader } from "../components/common/PageHeader";
import { DocumentUpload } from "../components/documents/DocumentUpload";
import { DocumentList } from "../components/documents/DocumentList";
import { SearchBar } from "../components/common/SearchBar";

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
                    <SearchBar
                        value={searchQuery}
                        onChange={setSearchQuery}
                        placeholder={t("documents.search.placeholder")}
                    />

                    <DocumentList searchQuery={searchQuery} />
                </div>
            </div>

            <AnimatePresence>
                {showUpload && <DocumentUpload onClose={handleCloseDocumentUploader} />}
            </AnimatePresence>
        </motion.div>
    );
};