import { useTranslation } from "react-i18next";
import { AnimatePresence } from "framer-motion";
import { AlertCircle, FileText } from "lucide-react";

import { useGetAllDocuments } from "../../hooks/institute/data/documents/useGetAllDocuments.ts";
import { DocumentRow } from "./DocumentRow";
import { EmptyState } from "../common/EmptyState";
import { LoadingSkeleton } from "../common/LoadingSkeleton";

interface DocumentListProps {
    searchQuery?: string;
}

export const DocumentList = ({ searchQuery = "" }: DocumentListProps) => {
    const { t } = useTranslation();
    const { data: documents, isLoading: isLoadingDocuments, error: errorRetrievingDocuments } =
        useGetAllDocuments();

    if (errorRetrievingDocuments) {
        return (
            <div className="card bg-base-100 shadow-lg">
                <div className="card-body">
                    <div role="alert" className="alert alert-error">
                        <AlertCircle size={24} aria-hidden="true" />
                        <div>
                            <h3 className="font-bold">{t("documents.list.error.title")}</h3>
                            <div className="text-sm">{t("documents.list.error.description")}</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    if (isLoadingDocuments) {
        return <LoadingSkeleton variant="list" count={3} />;
    }

    const docs = documents ?? [];
    const filtered = docs.filter((document) => {
        const query = searchQuery.trim().toLowerCase();
        if (!query) return true;
        const number = (document.number ?? "").toLowerCase();
        const title = (document.title ?? "").toLowerCase();
        return number.includes(query) || title.includes(query);
    });

    if (filtered.length === 0) {
        return (
            <EmptyState
                icon={FileText}
                title={t("documents.list.empty.title")}
                description={searchQuery ? t("documents.list.empty.noResults") : t("documents.list.empty.noDocuments")}
            />
        );
    }

    return (
        <div className="space-y-4">
            <AnimatePresence mode="popLayout">
                {filtered.map((document, index) => (
                    <DocumentRow key={document.id} document={document} index={index} />
                ))}
            </AnimatePresence>
        </div>
    );
};