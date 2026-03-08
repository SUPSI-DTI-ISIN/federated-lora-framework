import { SearchBar } from "../common/SearchBar";
import { useTranslation } from "react-i18next";

interface RealmSearchBarProps {
    value: string;
    onChange: (val: string) => void;
}

export const RealmSearchBar = ({ value, onChange }: RealmSearchBarProps) => {
    const { t } = useTranslation();
    
    return (
        <div className="my-10 flex justify-center">
            <SearchBar
                value={value}
                onChange={onChange}
                placeholder={t("realms.search.placeholder")}
            />
        </div>
    );
};
