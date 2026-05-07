import type {LucideIcon} from 'lucide-react';

interface EmptyStateProps {
    icon: LucideIcon;
    title: string;
    description?: string;
    action?: {
        label: string;
        onClick: () => void;
    };
}

export const EmptyState = ({
                               icon: Icon,
                               title,
                               description,
                               action,
                           }: EmptyStateProps) => {
    return (
        <div className="flex min-h-[400px] items-center justify-center p-8">
            <div className="flex max-w-md flex-col items-center text-center">
                <div className="mb-6 flex items-center justify-center rounded-full bg-base-200 p-6">
                    <Icon
                        size={48}
                        className="text-base-content/40"
                        strokeWidth={1.5}
                        aria-hidden="true"
                    />
                </div>

                <h3 className="mb-2 text-xl font-semibold text-base-content">
                    {title}
                </h3>

                {description && (
                    <p className="mb-6 text-base text-base-content/60">
                        {description}
                    </p>
                )}

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
