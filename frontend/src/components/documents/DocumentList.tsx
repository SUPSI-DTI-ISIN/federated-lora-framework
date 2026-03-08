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

/**
 * DocumentList Component
 * 
 * Refactored to use EmptyState and LoadingSkeleton components.
 * Preserves all existing business logic and data fetching hooks.
 * 
 * Requirements satisfied:
 * - 13.10: Render EmptyState when no documents
 * - 13.11: Render LoadingSkeleton when data is loading
 * - 13.12: Render DaisyUI alert with error icon on error
 * - 17.1: Render Loading_State using DaisyUI skeleton loaders
 * - 17.3: Render Error_State using DaisyUI alert component
 * - 17.4: Display error icon from Lucide
 * - 17.5: Display translated error message
 */
export const DocumentList = ({ searchQuery = "" }: DocumentListProps) => {
    const { t } = useTranslation();
    const { data: documents, isLoading: isLoadingDocuments, error: errorRetrievingDocuments } =
        useGetAllDocuments();

    // Error state
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

    // Loading state
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

    // Empty state
    if (filtered.length === 0) {
        return (
            <EmptyState
                icon={FileText}
                title={t("documents.list.empty.title")}
                description={searchQuery ? t("documents.list.empty.noResults") : t("documents.list.empty.noDocuments")}
            />
        );
    }

    // Document list
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