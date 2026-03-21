import {BarChart2, ChevronDown, ChevronUp, Table, Users} from "lucide-react";
import {useTranslation} from "react-i18next";
import type {Dispatch, SetStateAction} from "react";

interface InstituteTrainingParticipationCardHeaderProps {
    isOpen: boolean;
    setIsOpen: Dispatch<SetStateAction<boolean>>;
    viewMode: "table" | "chart";
    setViewMode: (viewMode: "table" | "chart") => void;
    institutesTrainingParticipationLen: number;
}

export const InstituteTrainingParticipationCardHeader = ({isOpen, setIsOpen, viewMode, setViewMode, institutesTrainingParticipationLen}: InstituteTrainingParticipationCardHeaderProps) => {
    const {t} = useTranslation();

    return (
        <div
            role="button"
            tabIndex={0}
            className="flex items-center px-6 py-4 w-full cursor-pointer"
            onClick={() => setIsOpen((prev) => !prev)}
        >
            <div className="flex items-center gap-3 min-w-0">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-secondary/10 text-secondary">
                    <Users size={20}/>
                </div>

                <span className="font-bold text-base-content truncate">
            {t("federatedLearning.participation.title")}
        </span>

                <span className="badge badge-secondary badge-sm">
            {institutesTrainingParticipationLen}
        </span>
            </div>

            <div className="flex items-center gap-2 ml-auto">
                {isOpen && (
                    <div
                        className="join"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            onClick={() => setViewMode("table")}
                            className={`join-item btn btn-xs ${
                                viewMode === "table" ? "btn-secondary" : "btn-ghost"
                            }`}
                        >
                            <Table size={14}/>
                        </button>

                        <button
                            onClick={() => setViewMode("chart")}
                            className={`join-item btn btn-xs ${
                                viewMode === "chart" ? "btn-secondary" : "btn-ghost"
                            }`}
                        >
                            <BarChart2 size={14}/>
                        </button>
                    </div>
                )}

                {isOpen ? (
                    <ChevronUp size={18} className="text-base-content/40"/>
                ) : (
                    <ChevronDown size={18} className="text-base-content/40"/>
                )}
            </div>
        </div>
    )
}