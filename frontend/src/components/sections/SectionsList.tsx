import { useState } from "react";
import type { SectionDTO } from "@isin/data-service-client";
import { SectionRow } from "./SectionRow";
import { useTranslation } from "react-i18next";


interface SectionsListProps {
    documentId: number
    sections: Array<SectionDTO>;
    selectedSections?: number[];
    onSelectSection?: (sectionId: number) => void;
}


export const SectionsList = ({ documentId, sections, selectedSections = [], onSelectSection }: SectionsListProps) => {
    const { t } = useTranslation();
    const [expandedIds, setExpandedIds] = useState<Array<number>>([]);


    const toggle = (id: number) => {
        setExpandedIds((prev) => (prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]));
    };


    if (!sections || sections.length === 0) {
        return (
            <div className="card bg-base-100 shadow-lg p-6 text-center">
                <p className="text-base-content/60">{t("sections.empty")}</p>
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
                    isSelected={selectedSections.includes(section.id)}
                    onSelect={onSelectSection ? () => onSelectSection(section.id) : undefined}
                />
            ))}
        </div>
    );
};