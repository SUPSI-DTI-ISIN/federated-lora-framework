import { Search } from "lucide-react";

interface SearchBarProps {
    value: string;
    onChange: (val: string) => void;
    placeholder: string;
}

export const SearchBar = ({ value, onChange, placeholder }: SearchBarProps) => (
    <div className="relative w-full max-w-2xl group">
        <div className="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none text-base-content/30 group-focus-within:text-primary transition-colors">
            <Search size={24} />
        </div>
        <input
            type="text"
            placeholder={placeholder}
            className="input input-bordered w-full h-14 pl-14 bg-base-200/40 border-base-content/10 focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all rounded-2xl text-lg shadow-sm"
            value={value}
            onChange={(e) => onChange(e.target.value)}
        />
    </div>
);
