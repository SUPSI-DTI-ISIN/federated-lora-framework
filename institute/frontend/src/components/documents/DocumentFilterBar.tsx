import { useTranslation } from "react-i18next";
import { Search } from "lucide-react";

type DocumentFilterBarProps = {
    value: string;
    onChange: (v: string) => void;
    onOpenUpload?: () => void;
};

export const DocumentFilterBar = ({ value, onChange, onOpenUpload }: DocumentFilterBarProps) => {
    const { t } = useTranslation();

    return (
        <div className="card bg-base-100 shadow-lg mb-6">
            <div className="card-body">
                <div className="flex flex-col md:flex-row md:items-center gap-4">
                    <div className="form-control flex-1">
                        <label htmlFor="doc-search" className="sr-only">
                            {t("documents.search.placeholder")}
                        </label>
                        <div className="input-group">
              <span className="bg-base-200" aria-hidden>
                <Search size={18} />
              </span>
                            <input
                                id="doc-search"
                                type="text"
                                placeholder={t("documents.search.placeholder")}
                                className="input input-bordered w-full"
                                value={value}
                                onChange={(e) => onChange(e.target.value)}
                                aria-label={t("documents.search.placeholder")}
                            />
                        </div>
                    </div>

                    {onOpenUpload && (
                        <div className="w-full md:w-auto flex justify-end">
                            <button
                                onClick={onOpenUpload}
                                className="btn btn-outline btn-primary"
                                aria-label={t("documents.uploadButton")}
                            >
                                {t("documents.uploadButton")}
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};