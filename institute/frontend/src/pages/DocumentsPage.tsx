import { useState } from "react";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import { FileText } from "lucide-react";

import { DocumentUpload } from "../components/documents/DocumentUpload";
import { DocumentList } from "../components/documents/DocumentList";
import { DocumentFilterBar } from "../components/documents/DocumentFilterBar";

export const DocumentsPage = () => {
    const { t } = useTranslation();
    const [searchQuery, setSearchQuery] = useState("");
    const [showUpload, setShowUpload] = useState(false);

    return (
        <div className="min-h-screen bg-linear-to-br from-base-100 via-base-200 to-base-100 py-8 px-4">
            <div className="max-w-7xl mx-auto">
                {/* Page Header */}
                <motion.div
                    initial={{ opacity: 0, y: -12 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mb-8"
                >
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <div>
                            <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
                                <FileText className="text-primary" size={36} />
                                <span>{t("documents.title")}</span>
                            </h1>
                            <p className="text-base-content/70">{t("documents.subtitle")}</p>
                        </div>

                        <div className="flex items-center gap-3">
                            <button
                                onClick={() => setShowUpload(true)}
                                className="btn btn-primary gap-2"
                                aria-label={t("documents.uploadButton")}
                            >
                                <FileText size={18} />
                                {t("documents.uploadButton")}
                            </button>
                        </div>
                    </div>
                </motion.div>

                {/* Filter Bar */}
                <DocumentFilterBar
                    value={searchQuery}
                    onChange={(v) => setSearchQuery(v)}
                    onOpenUpload={() => setShowUpload(true)}
                />

                {/* Document List */}
                <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.06 }}
                >
                    <DocumentList searchQuery={searchQuery} />
                </motion.div>
            </div>

            {/* Upload Modal */}
            <AnimatePresence>
                {showUpload && <DocumentUpload onClose={() => setShowUpload(false)} />}
            </AnimatePresence>
        </div>
    );
};