import {useTranslation} from 'react-i18next';
import {AnimatePresence} from 'framer-motion';
import {AlertCircle, FileIcon} from 'lucide-react';
import {useGetAllDocuments} from "../../hooks/documents/useGetAllDocuments.ts";
import {DocumentRow} from "./DocumentRow.tsx";

interface DocumentListProps {
    searchQuery: string;
}

export const DocumentList = ({ searchQuery }: DocumentListProps) => {
    const { t } = useTranslation();
    const { data: documents, isLoading: isLoadingDocuments, error: errorRetrievingDocuments } = useGetAllDocuments();

    if (errorRetrievingDocuments) {
        return (
            <div className="card bg-base-100 shadow-lg">
                <div className="card-body text-center py-16">
                    <AlertCircle className="mx-auto text-error mb-4" size={64} />
                    <h3 className="text-xl font-semibold mb-2">
                        {t('documents.list.error.title')}
                    </h3>
                    <p className="text-base-content/60">
                        {t('documents.list.error.description')}
                    </p>
                </div>
            </div>
        );
    }

    if (isLoadingDocuments) {
        return (
            <div className="space-y-4">
                {[1, 2, 3].map((i) => (
                    <div key={i} className="card bg-base-100 shadow-lg">
                        <div className="card-body">
                            <div className="flex gap-4">
                                <div className="skeleton w-12 h-12 rounded-lg"></div>
                                <div className="flex-1 space-y-2">
                                    <div className="skeleton h-4 w-3/4"></div>
                                    <div className="skeleton h-3 w-1/2"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    const filteredDocs = (documents || []).filter(doc => {
        return doc.id.toLowerCase().includes(searchQuery.toLowerCase());
    });

    if (filteredDocs.length === 0) {
        return (
            <div className="card bg-base-100 shadow-lg">
                <div className="card-body text-center py-16">
                    <FileIcon className="mx-auto text-base-content/30 mb-4" size={64} />
                    <h3 className="text-xl font-semibold mb-2">
                        {t('documents.list.empty.title')}
                    </h3>
                    <p className="text-base-content/60">
                        {searchQuery
                            ? t('documents.list.empty.noResults')
                            : t('documents.list.empty.noDocuments')}
                    </p>
                </div>
            </div>
        );
    }

    return (
        <>
            <div className="space-y-4">
                <AnimatePresence mode="popLayout">
                    {filteredDocs.map((document, index) => (
                        <DocumentRow document={document} index={index} />
                    ))}
                </AnimatePresence>
            </div>
        </>
    );
};