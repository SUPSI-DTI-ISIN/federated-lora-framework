import { useParams } from "react-router-dom";
import { useGetDocumentById } from "../hooks/institute/data/documents/useGetDocumentById.ts";
import { SectionsHeader } from "../components/sections/SectionsHeader";
import { SectionsList } from "../components/sections/SectionsList";


export const SectionsPage = () => {
    const { documentId } = useParams();
    const {
        data: document,
        isLoading: isLoadingDocument,
        error: errorLoadingDocument,
    } = useGetDocumentById(Number(documentId!));


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
                        <h3 className="text-xl font-semibold">Errore nel recupero del documento</h3>
                        <p className="text-base-content/60">Impossibile trovare il documento con l'ID fornito.</p>
                    </div>
                </div>
            </div>
        );
    }


    return (
        <div className="min-h-screen bg-base-100 py-8 px-4 sm:px-8">
            <div className="max-w-7xl mx-auto">
                <SectionsHeader title={document.title} number={document.number} />


                <div className="mt-6 bg-base-200/30 rounded-3xl p-4 border border-base-content/5">
                    <SectionsList documentId={document.id} sections={document.sections} />
                </div>
            </div>
        </div>
    );
};