import { useState } from "react";
import { useTranslation } from "react-i18next";
import { motion, AnimatePresence } from "framer-motion";
import { Files, Plus } from "lucide-react";

import { DocumentUpload } from "../components/documents/DocumentUpload";
import { DocumentList } from "../components/documents/DocumentList";
import { DocumentFilterBar } from "../components/documents/DocumentFilterBar";

export const DocumentsPage = () => {
    const { t } = useTranslation();
    const [searchQuery, setSearchQuery] = useState("");
    const [showUpload, setShowUpload] = useState(false);

    return (
        <div className="min-h-screen bg-base-100 py-8 px-4 sm:px-8">
            <div className="relative z-10 max-w-7xl mx-auto">

                {/* Header della Pagina */}
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10"
                >
                    <div className="flex items-center gap-4">
                        <div className="flex h-14 w-14 items-center justify-center bg-primary/10 rounded-2xl text-primary shadow-inner">
                            <Files size={32} />
                        </div>
                        <div>
                            <h1 className="text-4xl font-black tracking-tight text-base-content">
                                {t("documents.title")}
                            </h1>
                            <p className="text-base-content/60 font-medium">
                                {t("documents.subtitle")}
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={() => setShowUpload(true)}
                        className="btn btn-primary btn-md md:btn-lg shadow-xl shadow-primary/20 hover:scale-105 transition-all"
                    >
                        <Plus size={20} />
                        {t("documents.uploadButton")}
                    </button>
                </motion.div>

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
                {showUpload && <DocumentUpload onClose={() => setShowUpload(false)} />}
            </AnimatePresence>
        </div>
    );
};