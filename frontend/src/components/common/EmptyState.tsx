import type { LucideIcon } from 'lucide-react';

interface EmptyStateProps {
  icon: LucideIcon;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

/**
 * EmptyState Component
 * 
 * A reusable empty state component that displays when no data is available.
 * 
 * Features:
 * - Displays icon with title and optional description
 * - Supports optional action button with label and onClick handler
 * - Uses centered layout with generous whitespace
 * - Uses Design_System typography (Plus Jakarta Sans for headings, DM Sans for body)
 * - Uses Design_System spacing and colors
 * - Fully responsive layout
 * 
 * Requirements satisfied:
 * - 16.3: Provide EmptyState reusable component
 * - 16.10: Pure presentation component without business logic
 * 
 * @example
 * ```tsx
 * <EmptyState
 *   icon={MessageSquare}
 *   title="No chats yet"
 *   description="Start a new conversation to get started"
 *   action={{
 *     label: "New Chat",
 *     onClick: handleNewChat
 *   }}
 * />
 * ```
 */
export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="flex min-h-[400px] items-center justify-center p-8">
      <div className="flex max-w-md flex-col items-center text-center">
        {/* Icon */}
        <div className="mb-6 flex items-center justify-center rounded-full bg-base-200 p-6">
          <Icon
            size={48}
            className="text-base-content/40"
            strokeWidth={1.5}
            aria-hidden="true"
          />
        </div>

        {/* Title */}
        <h3 className="mb-2 text-xl font-semibold text-base-content">
          {title}
        </h3>

        {/* Description */}
        {description && (
          <p className="mb-6 text-base text-base-content/60">
            {description}
          </p>
        )}

        {/* Action button */}
        {action && (
          <button
            onClick={action.onClick}
            className="btn btn-primary"
            type="button"
          >
            {action.label}
          </button>
        )}
      </div>
    </div>
  );
}
