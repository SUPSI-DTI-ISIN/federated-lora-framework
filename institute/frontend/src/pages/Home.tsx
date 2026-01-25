import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { FileText, MessageSquare, Zap, Shield, Users, TrendingUp } from 'lucide-react';
import mimirLogo from '../assets/mimir-logo.png';

export const Home = () => {
    const { t } = useTranslation();

    const features = [
        { icon: FileText, title: 'home.features.upload.title', description: 'home.features.upload.description', color: 'bg-blue-500/10 text-blue-600 dark:text-blue-400' },
        { icon: Zap, title: 'home.features.finetune.title', description: 'home.features.finetune.description', color: 'bg-amber-500/10 text-amber-600 dark:text-amber-400' },
        { icon: MessageSquare, title: 'home.features.chat.title', description: 'home.features.chat.description', color: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400' },
        { icon: Shield, title: 'home.features.federated.title', description: 'home.features.federated.description', color: 'bg-purple-500/10 text-purple-600 dark:text-purple-400' },
        { icon: Users, title: 'home.features.collaborative.title', description: 'home.features.collaborative.description', color: 'bg-rose-500/10 text-rose-600 dark:text-rose-400' },
        { icon: TrendingUp, title: 'home.features.improve.title', description: 'home.features.improve.description', color: 'bg-cyan-500/10 text-cyan-600 dark:text-cyan-400' },
    ];

    return (
        <div className="min-h-screen bg-base-100 selection:bg-primary/20">
            <section className="relative pt-20 pb-24 lg:pt-32 lg:pb-40 px-6 overflow-hidden">
                <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/4 w-96 h-96 bg-primary/5 blur-[120px] rounded-full" />

                <div className="max-w-7xl mx-auto">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                        <motion.div
                            initial={{ opacity: 0, x: -30 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.8 }}
                            className="text-left"
                        >
                            <h1 className="text-5xl md:text-7xl font-black text-base-content tracking-tight leading-tight mb-6">
                                {t('home.hero.title')}
                            </h1>
                            <p className="text-xl md:text-2xl text-base-content/70 mb-10 leading-relaxed max-w-2xl">
                                {t('home.hero.subtitle')}
                            </p>
                        </motion.div>

                        <motion.div
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 1, ease: "easeOut" }}
                            className="flex justify-center lg:justify-end"
                        >
                            <div className="relative group">
                                <div className="absolute -inset-4 bg-primary/10 rounded-full blur-3xl group-hover:bg-primary/20 transition-all duration-700" />
                                <img
                                    src={mimirLogo}
                                    alt="Mimir Engine"
                                    className="relative h-64 md:h-96 w-auto object-contain drop-shadow-[0_20px_50px_rgba(0,0,0,0.1)] dark:drop-shadow-[0_20px_50px_rgba(255,255,255,0.05)]"
                                />
                            </div>
                        </motion.div>
                    </div>
                </div>
            </section>

            <section className="py-24 px-6 bg-base-200/50 border-t border-base-content/5">
                <div className="max-w-7xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <h2 className="text-4xl md:text-5xl font-bold text-base-content mb-6">
                            {t('home.features.title')}
                        </h2>
                        <p className="text-lg text-base-content/60 max-w-2xl mx-auto">
                            {t('home.features.subtitle')}
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {features.map((feature, index) => {
                            const Icon = feature.icon;
                            return (
                                <motion.div
                                    key={index}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    viewport={{ once: true }}
                                    transition={{ delay: index * 0.05 }}
                                    className="card bg-base-100 border border-base-content/5 shadow-sm hover:shadow-xl hover:-translate-y-2 transition-all duration-300"
                                >
                                    <div className="card-body p-8">
                                        <div className={`w-12 h-12 rounded-xl ${feature.color} flex items-center justify-center mb-6`}>
                                            <Icon size={24} />
                                        </div>
                                        <h3 className="text-xl font-bold text-base-content mb-3">
                                            {t(feature.title)}
                                        </h3>
                                        <p className="text-base-content/70 leading-relaxed text-sm">
                                            {t(feature.description)}
                                        </p>
                                    </div>
                                </motion.div>
                            );
                        })}
                    </div>
                </div>
            </section>
        </div>
    );
};