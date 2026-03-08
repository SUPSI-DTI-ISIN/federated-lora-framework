import type { LucideIcon } from 'lucide-react';

interface PageHeaderProps {
  icon?: LucideIcon;
  title: string;
  subtitle?: string;
  action?: {
    label: string;
    icon?: LucideIcon;
    onClick: () => void;
  };
}

/**
 * PageHeader Component
 * 
 * A reusable page header component that provides consistent page headers across all pages.
 * 
 * Features:
 * - Displays optional icon with title
 * - Shows optional subtitle text
 * - Supports optional action button with icon and onClick handler
 * - Uses Design_System typography (Plus Jakarta Sans for headings, DM Sans for body)
 * - Uses Design_System spacing (p-6 for sections, gap-4 for elements)
 * - Fully responsive layout
 * 
 * Requirements satisfied:
 * - 16.2: Provide PageHeader reusable component
 * - 16.9: Pure presentation component without business logic
 * 
 * @example
 * ```tsx
 * <PageHeader
 *   icon={FileText}
 *   title="Documents"
 *   subtitle="Manage your PDF documents"
 *   action={{
 *     label: "Upload",
 *     icon: Upload,
 *     onClick: handleUpload
 *   }}
 * />
 * ```
 */
export function PageHeader({
  icon: Icon,
  title,
  subtitle,
  action,
}: PageHeaderProps) {
  return (
    <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      {/* Title section */}
      <div className="flex items-start gap-3">
        {Icon && (
          <div className="mt-1 flex-shrink-0">
            <Icon
              size={32}
              className="text-primary"
              strokeWidth={2}
              aria-hidden="true"
            />
          </div>
        )}
        <div>
          <h1 className="text-3xl font-bold text-base-content">
            {title}
          </h1>
          {subtitle && (
            <p className="mt-1 text-base text-base-content/70">
              {subtitle}
            </p>
          )}
        </div>
      </div>

      {/* Action button */}
      {action && (
        <button
          onClick={action.onClick}
          className="btn btn-primary gap-2"
          type="button"
        >
          {action.icon && (
            <action.icon
              size={16}
              strokeWidth={2}
              aria-hidden="true"
            />
          )}
          {action.label}
        </button>
      )}
    </div>
  );
}
