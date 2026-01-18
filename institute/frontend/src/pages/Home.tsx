import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FileText, MessageSquare, Zap, Shield, Users, TrendingUp } from 'lucide-react';

export const Home = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();

    const features = [
        {
            icon: FileText,
            title: 'home.features.upload.title',
            description: 'home.features.upload.description',
            color: 'text-primary'
        },
        {
            icon: Zap,
            title: 'home.features.finetune.title',
            description: 'home.features.finetune.description',
            color: 'text-secondary'
        },
        {
            icon: MessageSquare,
            title: 'home.features.chat.title',
            description: 'home.features.chat.description',
            color: 'text-accent'
        },
        {
            icon: Shield,
            title: 'home.features.federated.title',
            description: 'home.features.federated.description',
            color: 'text-success'
        },
        {
            icon: Users,
            title: 'home.features.collaborative.title',
            description: 'home.features.collaborative.description',
            color: 'text-info'
        },
        {
            icon: TrendingUp,
            title: 'home.features.improve.title',
            description: 'home.features.improve.description',
            color: 'text-warning'
        },
    ];

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { y: 20, opacity: 0 },
        visible: {
            y: 0,
            opacity: 1
        }
    };

    return (
        <div className="min-h-screen bg-linear-to-br from-base-100 via-base-200 to-base-100">
            {/* Hero Section */}
            <section className="pt-20 pb-16 px-4">
                <div className="max-w-6xl mx-auto text-center">
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6 }}
                    >
                        <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">
                            {t('home.hero.title')}
                        </h1>
                        <p className="text-xl md:text-2xl text-base-content/70 mb-8 max-w-3xl mx-auto">
                            {t('home.hero.subtitle')}
                        </p>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.2 }}
                        className="flex flex-wrap gap-4 justify-center"
                    >
                        <button
                            onClick={() => navigate('/documents')}
                            className="btn btn-primary btn-lg gap-2"
                        >
                            <FileText size={20} />
                            {t('home.hero.cta.documents')}
                        </button>
                        <button
                            onClick={() => navigate('/chat')}
                            className="btn btn-outline btn-lg gap-2"
                        >
                            <MessageSquare size={20} />
                            {t('home.hero.cta.chat')}
                        </button>
                    </motion.div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-16 px-4 bg-base-200/50">
                <div className="max-w-6xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="text-center mb-12"
                    >
                        <h2 className="text-4xl font-bold mb-4">{t('home.features.title')}</h2>
                        <p className="text-lg text-base-content/70">
                            {t('home.features.subtitle')}
                        </p>
                    </motion.div>

                    <motion.div
                        variants={containerVariants}
                        initial="hidden"
                        whileInView="visible"
                        viewport={{ once: true }}
                        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
                    >
                        {features.map((feature, index) => {
                            const Icon = feature.icon;
                            return (
                                <motion.div
                                    key={index}
                                    variants={itemVariants}
                                    className="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow"
                                >
                                    <div className="card-body">
                                        <div className={`w-12 h-12 rounded-lg bg-base-200 flex items-center justify-center ${feature.color} mb-4`}>
                                            <Icon size={24} />
                                        </div>
                                        <h3 className="card-title text-lg">
                                            {t(feature.title)}
                                        </h3>
                                        <p className="text-base-content/70">
                                            {t(feature.description)}
                                        </p>
                                    </div>
                                </motion.div>
                            );
                        })}
                    </motion.div>
                </div>
            </section>

            {/* How it Works Section */}
            <section className="py-16 px-4">
                <div className="max-w-4xl mx-auto">
                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        viewport={{ once: true }}
                        className="text-center mb-12"
                    >
                        <h2 className="text-4xl font-bold mb-4">{t('home.howItWorks.title')}</h2>
                    </motion.div>

                    <div className="space-y-8">
                        {[1, 2, 3].map((step) => (
                            <motion.div
                                key={step}
                                initial={{ opacity: 0, x: step % 2 === 0 ? 50 : -50 }}
                                whileInView={{ opacity: 1, x: 0 }}
                                viewport={{ once: true }}
                                transition={{ duration: 0.5 }}
                                className="flex items-start gap-6"
                            >
                                <div className="shrink-0">
                                    <div className="w-12 h-12 rounded-full bg-primary text-primary-content flex items-center justify-center font-bold text-xl">
                                        {step}
                                    </div>
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold mb-2">
                                        {t(`home.howItWorks.step${step}.title`)}
                                    </h3>
                                    <p className="text-base-content/70">
                                        {t(`home.howItWorks.step${step}.description`)}
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
};