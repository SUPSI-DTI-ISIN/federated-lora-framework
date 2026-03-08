import {Building2} from "lucide-react";

interface InstituteBadgeProps {
    instituteName: string;
    className?: string;
}

export const InstituteBadge = ({instituteName, className = ""}: InstituteBadgeProps) => {
    const shouldTruncate = instituteName.length > 20;
    const displayName = shouldTruncate
        ? `${instituteName.substring(0, 20)}...`
        : instituteName;

    const badgeContent = (
        <div
            className={`
        inline-flex items-center gap-2 px-3 py-1.5 rounded-full
        border border-indigo-200 bg-indigo-50 text-indigo-700
        dark:border-indigo-700 dark:bg-indigo-950 dark:text-indigo-300
        text-sm font-medium
        ${className}
      `}
            role="status"
            aria-label={`Institute: ${instituteName}`}
        >
            <Building2 size={14} strokeWidth={2} aria-hidden="true"/>
            <span className={shouldTruncate ? "truncate" : ""}>
        {displayName}
      </span>
        </div>
    );

    if (shouldTruncate) {
        return (
            <div className="tooltip tooltip-bottom" data-tip={instituteName}>
                {badgeContent}
            </div>
        );
    }

    return badgeContent;
}
