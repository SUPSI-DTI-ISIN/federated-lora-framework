import { useState } from "react";
import type { SectionDTO } from "@isin/data-service-client";
import { SectionRow } from "./SectionRow";


interface SectionsListProps {
    documentId: number
    sections: Array<SectionDTO>;
    onDeleteSection?: (sectionId: number) => void;
}


export const SectionsList = ({ documentId, sections }: SectionsListProps) => {
    const [expandedIds, setExpandedIds] = useState<Array<number>>([]);


    const toggle = (id: number) => {
        setExpandedIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
    };


    if (!sections || sections.length === 0) {
        return (
            <div className="card bg-base-100 shadow-lg p-6 text-center">
                <p className="text-base-content/60">Nessuna sezione disponibile per questo documento.</p>
            </div>
        );
    }


    return (
        <div className="space-y-3">
            {sections.map((section) => (
                <SectionRow
                    key={section.id}
                    section={section}
                    documentId={documentId}
                    expanded={expandedIds.includes(section.id)}
                    onToggle={() => toggle(section.id)}
                />
            ))}
        </div>
    );
};