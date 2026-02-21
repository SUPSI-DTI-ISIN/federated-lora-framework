import { useTranslation } from "react-i18next";
import { Search } from "lucide-react";

type DocumentFilterBarProps = {
    value: string;
    onChange: (v: string) => void;
};

export const DocumentFilterBar = ({ value, onChange }: DocumentFilterBarProps) => {
    const { t } = useTranslation();

    return (
        <div className="w-full">
            <div className="relative group">
                <div className="absolute inset-y-0 left-5 flex items-center pointer-events-none text-base-content/30 group-focus-within:text-primary transition-colors">
                    <Search size={22} />
                </div>
                <input
                    id="doc-search"
                    type="text"
                    placeholder={t("documents.search.placeholder")}
                    className="input input-lg w-full pl-14 bg-base-200/50 border-none focus:bg-base-100 focus:ring-2 focus:ring-primary/20 transition-all rounded-2xl text-lg h-16"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                />
            </div>
        </div>
    );
};