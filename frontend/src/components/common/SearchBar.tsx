import { useTranslation } from "react-i18next";
import { Search } from "lucide-react";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholderKey: string;
}

export const SearchBar = ({ value, onChange, placeholderKey }: SearchBarProps) => {
  const { t } = useTranslation();

  return (
    <div className="relative w-full max-w-md">
      <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none text-base-content/40">
        <Search size={20} />
      </div>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={t(placeholderKey)}
        className="input input-bordered w-full pl-12 bg-base-100 focus:outline-none focus:ring-2 focus:ring-primary/20 transition-all"
      />
    </div>
  );
};
