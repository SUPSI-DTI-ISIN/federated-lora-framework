import { Building2 } from "lucide-react";

interface InstituteBadgeProps {
  instituteName: string;
  className?: string;
}

/**
 * InstituteBadge Component
 * 
 * A reusable badge component that displays the institute name in the navbar.
 * 
 * Features:
 * - Displays institute name with Building2 icon prefix
 * - Uses theme-specific indigo colors (light: border-indigo-200 bg-indigo-50 text-indigo-700, dark: border-indigo-700 bg-indigo-950 text-indigo-300)
 * - Truncates long names (>20 characters) with ellipsis and shows full name in tooltip
 * - Uses Design_System typography (DM Sans medium font at text-sm size)
 * - Fully accessible with proper ARIA labels
 * - Not clickable (display only)
 * 
 * Requirements satisfied:
 * - 5.1: Read INSTITUTE_NAME from realm context
 * - 5.2: Display between app logo and navbar spacer
 * - 5.3: Render as pill/badge with indigo border and text
 * - 5.4: Light theme colors (border-indigo-200 bg-indigo-50 text-indigo-700)
 * - 5.5: Dark theme colors (border-indigo-700 bg-indigo-950 text-indigo-300)
 * - 5.6: Use DM Sans medium font at text-sm size
 * - 5.7: Display Building2 icon prefix at 14px size
 * - 5.8: Truncate long names with ellipsis and tooltip
 * - 5.9: Visible on all pages
 * - 5.10: Not clickable
 * - 16.7: Provide InstituteBadge reusable component
 * - 16.14: Only display data passed via props
 * 
 * @example
 * ```tsx
 * <InstituteBadge instituteName="University of Technology" />
 * <InstituteBadge instituteName="MIT" />
 * ```
 */
export function InstituteBadge({ instituteName, className = "" }: InstituteBadgeProps) {
  // Determine if name should be truncated (>20 characters)
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
      <Building2 size={14} strokeWidth={2} aria-hidden="true" />
      <span className={shouldTruncate ? "truncate" : ""}>
        {displayName}
      </span>
    </div>
  );

  // Wrap in tooltip if name is truncated
  if (shouldTruncate) {
    return (
      <div className="tooltip tooltip-bottom" data-tip={instituteName}>
        {badgeContent}
      </div>
    );
  }

  return badgeContent;
}
