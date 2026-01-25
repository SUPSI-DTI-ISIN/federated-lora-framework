import { useTranslation } from "react-i18next";

type AdapterFilterBarProps = {
    query: string;
    onQueryChange: (v: string) => void;
    localOnly: boolean;
    onLocalOnlyChange: (v: boolean) => void;
};

export const AdapterFilterBar = ({ query, onQueryChange, localOnly, onLocalOnlyChange }: AdapterFilterBarProps) => {
    const { t } = useTranslation();

    return (
        <div className="flex flex-col md:flex-row gap-2 items-center">
            <input
                type="text"
                placeholder={t("adapters.filter.searchPlaceholder")}
                value={query}
                onChange={(e) => onQueryChange(e.target.value)}
                className="input input-bordered w-full md:w-64"
                aria-label={t("adapters.filter.searchPlaceholder")}
            />
            <label className="flex items-center gap-2 text-sm">
                <input
                    type="checkbox"
                    checked={localOnly}
                    onChange={(e) => onLocalOnlyChange(e.target.checked)}
                    className="checkbox"
                />
                <span>{t("adapters.filter.localOnly")}</span>
            </label>
        </div>
    );
};
