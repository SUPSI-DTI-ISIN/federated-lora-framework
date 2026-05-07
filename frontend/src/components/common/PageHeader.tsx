import {type LucideIcon} from 'lucide-react';
import {motion} from "framer-motion";

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
            <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-5 mb-8"
            >
                {Icon && (
                    <div className="flex h-16 w-16 items-center justify-center bg-info/10 rounded-2xl text-info shadow-inner">
                        <Icon size={36} />
                    </div>
                )}
                <div>
                    <h1 className="text-4xl font-black tracking-tight text-base-content leading-none mb-2">
                        {title}
                    </h1>
                    <p className="text-lg text-base-content/60 font-medium">
                        {subtitle}
                    </p>
                </div>
            </motion.div>

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
