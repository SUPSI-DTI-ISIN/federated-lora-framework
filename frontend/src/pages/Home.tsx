import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { FileText, MessageSquare, Cpu } from 'lucide-react';
import mimirLogo from '../assets/mimir-logo.png';
import { useAuthWrapper } from '../hooks/auth/useAuthWrapper';

export const Home = () => {
    const { t } = useTranslation();
    const { user, isAuthenticated } = useAuthWrapper();

    // Extract user name from OIDC profile
    const userName = user?.profile?.preferred_username || user?.profile?.name || user?.profile?.sub || t('common.user');

    // Mock user data - in a real app, this would come from an API
    // For now, we'll show stats when user is authenticated
    const hasUserData = isAuthenticated;

    return (
        <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25 }}
            className="min-h-full"
        >
            {/* Welcome Hero Section */}
            <div className="mb-8 text-center">
                <h1 className="text-4xl md:text-5xl font-bold text-base-content mb-2">
                    {t('home.welcome', { name: userName })}
                </h1>
                <p className="text-lg text-base-content/70">
                    {t('home.tagline')}
                </p>
            </div>

            {/* Content: Stats or Empty State */}
            {hasUserData ? (
                <div className="max-w-4xl mx-auto">
                    {/* Summary Stats Cards */}
                    <div className="stats stats-vertical lg:stats-horizontal shadow-lg w-full bg-base-100 border border-base-content/10">
                        <div className="stat">
                            <div className="stat-figure text-indigo-600 dark:text-indigo-400">
                                <FileText size={32} strokeWidth={2} />
                            </div>
                            <div className="stat-title">{t('documents.title')}</div>
                            <div className="stat-value text-indigo-600 dark:text-indigo-400">0</div>
                            <div className="stat-desc">{t('documents.empty')}</div>
                        </div>

                        <div className="stat">
                            <div className="stat-figure text-indigo-600 dark:text-indigo-400">
                                <MessageSquare size={32} strokeWidth={2} />
                            </div>
                            <div className="stat-title">{t('chat.title')}</div>
                            <div className="stat-value text-indigo-600 dark:text-indigo-400">0</div>
                            <div className="stat-desc">{t('chat.empty')}</div>
                        </div>

                        <div className="stat">
                            <div className="stat-figure text-indigo-600 dark:text-indigo-400">
                                <Cpu size={32} strokeWidth={2} />
                            </div>
                            <div className="stat-title">{t('adapters.title')}</div>
                            <div className="stat-value text-indigo-600 dark:text-indigo-400">0</div>
                            <div className="stat-desc">{t('adapters.empty')}</div>
                        </div>
                    </div>

                    {/* Features Grid */}
                    <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div className="card bg-base-100 border border-indigo-200 dark:border-indigo-700 shadow-sm hover:shadow-md transition-shadow">
                            <div className="card-body p-6">
                                <div className="flex items-center gap-3 mb-3">
                                    <div className="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400">
                                        <FileText size={20} strokeWidth={2} />
                                    </div>
                                    <h3 className="text-lg font-semibold text-base-content">
                                        {t('home.features.upload.title')}
                                    </h3>
                                </div>
                                <p className="text-sm text-base-content/70">
                                    {t('home.features.upload.description')}
                                </p>
                            </div>
                        </div>

                        <div className="card bg-base-100 border border-indigo-200 dark:border-indigo-700 shadow-sm hover:shadow-md transition-shadow">
                            <div className="card-body p-6">
                                <div className="flex items-center gap-3 mb-3">
                                    <div className="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400">
                                        <Cpu size={20} strokeWidth={2} />
                                    </div>
                                    <h3 className="text-lg font-semibold text-base-content">
                                        {t('home.features.finetune.title')}
                                    </h3>
                                </div>
                                <p className="text-sm text-base-content/70">
                                    {t('home.features.finetune.description')}
                                </p>
                            </div>
                        </div>

                        <div className="card bg-base-100 border border-indigo-200 dark:border-indigo-700 shadow-sm hover:shadow-md transition-shadow">
                            <div className="card-body p-6">
                                <div className="flex items-center gap-3 mb-3">
                                    <div className="p-2 rounded-lg bg-indigo-50 dark:bg-indigo-950 text-indigo-600 dark:text-indigo-400">
                                        <MessageSquare size={20} strokeWidth={2} />
                                    </div>
                                    <h3 className="text-lg font-semibold text-base-content">
                                        {t('home.features.chat.title')}
                                    </h3>
                                </div>
                                <p className="text-sm text-base-content/70">
                                    {t('home.features.chat.description')}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="max-w-2xl mx-auto">
                    {/* Empty State with Logo */}
                    <div className="flex min-h-[400px] items-center justify-center p-8">
                        <div className="flex max-w-md flex-col items-center text-center">
                            {/* Logo */}
                            <div className="mb-6 flex items-center justify-center">
                                <img
                                    src={mimirLogo}
                                    alt="Mimir Engine"
                                    className="h-32 w-auto object-contain"
                                />
                            </div>

                            {/* Title */}
                            <h3 className="mb-2 text-2xl font-semibold text-base-content">
                                {t('home.tagline')}
                            </h3>

                            {/* Description */}
                            <p className="text-base text-base-content/60">
                                {t('home.description')}
                            </p>
                        </div>
                    </div>
                </div>
            )}
        </motion.div>
    );
};