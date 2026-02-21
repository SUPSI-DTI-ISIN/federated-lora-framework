import { useTranslation } from "react-i18next";
import {Search} from "lucide-react";

type AdapterFilterBarProps = {
    query: string;
    onQueryChange: (v: string) => void;
    localOnly: boolean;
    onLocalOnlyChange: (v: boolean) => void;
};

export const AdapterFilterBar = ({ query, onQueryChange, localOnly, onLocalOnlyChange }: AdapterFilterBarProps) => {
    const { t } = useTranslation();

    return (
        <div className="flex flex-col sm:flex-row items-center gap-4 p-1">
            <div className="relative w-full sm:w-80">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-base-content/30" size={18} />
                <input
                    type="text"
                    placeholder={t("adapters.filter.searchPlaceholder")}
                    value={query}
                    onChange={(e) => onQueryChange(e.target.value)}
                    className="input input-ghost w-full pl-12 bg-base-100 focus:bg-base-100 rounded-xl border-none focus:ring-2 focus:ring-secondary/20"
                />
            </div>

            <div className="divider divider-horizontal hidden sm:flex mx-0" />

            <label className="flex items-center gap-3 cursor-pointer select-none px-4 py-2 hover:bg-base-100 rounded-xl transition-colors w-full sm:w-auto justify-between sm:justify-start">
                <span className="text-sm font-bold text-base-content/70 uppercase tracking-wider">
                    {t("adapters.filter.localOnly")}
                </span>
                <input
                    type="checkbox"
                    checked={localOnly}
                    onChange={(e) => onLocalOnlyChange(e.target.checked)}
                    className="toggle toggle-secondary"
                />
            </label>
        </div>
    );
};