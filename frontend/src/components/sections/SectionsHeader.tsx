import { AlignLeft } from "lucide-react";
import {useTranslation} from "react-i18next";

interface SectionsHeaderProps {
    title: string;
    number: string;
}

export const SectionsHeader = ({ title, number }: SectionsHeaderProps) => {
    const {t} = useTranslation();

    return (
        <div className="flex items-start gap-5">
            <div className="shrink-0 pt-0.5">
                <div className="flex h-16 w-16 items-center justify-center bg-info/10 rounded-2xl text-info shadow-inner">
                    <AlignLeft size={36} />
                </div>
            </div>

            <div className="min-w-0 flex-1 border-l border-base-300 pl-5">
                <div className="flex items-baseline gap-3 flex-wrap mb-0.5">
                    <h1 className="text-xl font-medium tracking-tight text-base-content">
                        {title}
                    </h1>
                    <span className="text-[11px] font-mono text-base-content/40 bg-base-200 border border-base-300 px-2 py-0.5 rounded tracking-widest whitespace-nowrap">
                        #{number}
                    </span>
                </div>

                <p className="text-sm text-base-content/60 leading-relaxed max-w-2xl">
                    {t("sections.header.description")}
                </p>
            </div>
        </div>
    );
};