import type {LucideIcon} from 'lucide-react';

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

export const PageHeader = ({
                               icon: Icon,
                               title,
                               subtitle,
                               action,
                           }: PageHeaderProps) => {
    return (
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
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
