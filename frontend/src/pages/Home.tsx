import {useTranslation} from 'react-i18next';
import {motion} from 'framer-motion';
import {
    FileText,
    MessageSquare,
    Cpu,
    Users,
    TrendingUp,
    Sparkles,
    Lock,
    Zap,
    ArrowRight
} from 'lucide-react';
import {Link} from 'react-router-dom';
import {useAuthWrapper} from '../hooks/auth/useAuthWrapper';

export const Home = () => {
    const {t} = useTranslation();
    const {user, isAuthenticated, isDepartmentAdmin} = useAuthWrapper();

    const userName = user?.profile?.preferred_username || user?.profile?.name || t('home.guest');

    const containerVariants = {
        hidden: {opacity: 0},
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: {opacity: 0, y: 20},
        visible: {
            opacity: 1,
            y: 0,
            transition: {duration: 0.5}
        }
    };

    return (
        <div className="min-h-screen w-full bg-gradient-to-br from-base-100 via-base-200 to-base-100">
            {/* Hero Section */}
            <motion.section
                initial="hidden"
                animate="visible"
                variants={containerVariants}
                className="relative overflow-hidden px-6 py-20 lg:py-32"
            >
                {/* Background decoration */}
                <div className="absolute inset-0 overflow-hidden pointer-events-none">
                    <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/10 rounded-full blur-3xl"/>
                    <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-secondary/10 rounded-full blur-3xl"/>
                </div>

                <div className="relative max-w-7xl mx-auto">
                    <motion.div variants={itemVariants} className="text-center mb-12">
                        {isAuthenticated && (
                            <motion.div
                                initial={{opacity: 0, scale: 0.9}}
                                animate={{opacity: 1, scale: 1}}
                                className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary mb-6"
                            >
                                <Sparkles size={16}/>
                                <span className="text-sm font-medium">{t('home.welcome', {name: userName})}</span>
                            </motion.div>
                        )}

                        <h1 className="text-5xl md:text-7xl font-bold text-base-content mb-6 leading-tight">
                            {t('home.hero.title')}
                        </h1>

                        <p className="text-xl md:text-2xl text-base-content/70 max-w-3xl mx-auto mb-10">
                            {t('home.hero.subtitle')}
                        </p>

                        {isAuthenticated && !isDepartmentAdmin && (
                            <motion.div
                                variants={itemVariants}
                                className="flex flex-wrap items-center justify-center gap-4"
                            >
                                <Link to="/documents">
                                    <button
                                        className="btn btn-primary btn-lg gap-2 shadow-lg hover:shadow-xl transition-all">
                                        <FileText size={20}/>
                                        {t('home.hero.cta.documents')}
                                        <ArrowRight size={18}/>
                                    </button>
                                </Link>
                                <Link to="/chat">
                                    <button className="btn btn-outline btn-lg gap-2">
                                        <MessageSquare size={20}/>
                                        {t('home.hero.cta.chat')}
                                    </button>
                                </Link>
                            </motion.div>
                        )}
                    </motion.div>
                </div>
            </motion.section>

            {/* Features Grid */}
            <motion.section
                initial="hidden"
                whileInView="visible"
                viewport={{once: true, margin: "-100px"}}
                variants={containerVariants}
                className="px-6 py-20 bg-base-100"
            >
                <div className="max-w-7xl mx-auto">
                    <motion.div variants={itemVariants} className="text-center mb-16">
                        <h2 className="text-4xl md:text-5xl font-bold text-base-content mb-4">
                            {t('home.features.title')}
                        </h2>
                        <p className="text-lg text-base-content/70 max-w-2xl mx-auto">
                            {t('home.features.subtitle')}
                        </p>
                    </motion.div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {[
                            {
                                icon: FileText,
                                titleKey: 'home.features.upload.title',
                                descKey: 'home.features.upload.description',
                                color: 'text-blue-500',
                                bgColor: 'bg-blue-500/10'
                            },
                            {
                                icon: Cpu,
                                titleKey: 'home.features.finetune.title',
                                descKey: 'home.features.finetune.description',
                                color: 'text-purple-500',
                                bgColor: 'bg-purple-500/10'
                            },
                            {
                                icon: MessageSquare,
                                titleKey: 'home.features.chat.title',
                                descKey: 'home.features.chat.description',
                                color: 'text-green-500',
                                bgColor: 'bg-green-500/10'
                            },
                            {
                                icon: Lock,
                                titleKey: 'home.features.federated.title',
                                descKey: 'home.features.federated.description',
                                color: 'text-red-500',
                                bgColor: 'bg-red-500/10'
                            },
                            {
                                icon: Users,
                                titleKey: 'home.features.collaborative.title',
                                descKey: 'home.features.collaborative.description',
                                color: 'text-orange-500',
                                bgColor: 'bg-orange-500/10'
                            },
                            {
                                icon: TrendingUp,
                                titleKey: 'home.features.improve.title',
                                descKey: 'home.features.improve.description',
                                color: 'text-teal-500',
                                bgColor: 'bg-teal-500/10'
                            }
                        ].map((feature, index) => (
                            <motion.div
                                key={index}
                                variants={itemVariants}
                                whileHover={{y: -8, transition: {duration: 0.2}}}
                                className="group relative"
                            >
                                <div
                                    className="h-full p-8 rounded-2xl bg-base-100 border border-base-content/10 hover:border-primary/30 transition-all shadow-lg hover:shadow-2xl">
                                    <div className={`inline-flex p-4 rounded-xl ${feature.bgColor} mb-6`}>
                                        <feature.icon className={`${feature.color}`} size={28} strokeWidth={2}/>
                                    </div>
                                    <h3 className="text-xl font-bold text-base-content mb-3">
                                        {t(feature.titleKey)}
                                    </h3>
                                    <p className="text-base-content/70 leading-relaxed">
                                        {t(feature.descKey)}
                                    </p>
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </div>
            </motion.section>

            {/* How It Works */}
            <motion.section
                initial="hidden"
                whileInView="visible"
                viewport={{once: true, margin: "-100px"}}
                variants={containerVariants}
                className="px-6 py-20 bg-base-200/50"
            >
                <div className="max-w-7xl mx-auto">
                    <motion.div variants={itemVariants} className="text-center mb-16">
                        <h2 className="text-4xl md:text-5xl font-bold text-base-content mb-4">
                            {t('home.howItWorks.title')}
                        </h2>
                    </motion.div>

                    {/* User Workflow */}
                    {!isDepartmentAdmin && (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
                            {/* Connection lines for desktop */}
                            <div
                                className="hidden md:block absolute top-1/4 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-primary/30 to-transparent"/>

                            {[
                                {
                                    step: '01',
                                    titleKey: 'home.howItWorks.user.step1.title',
                                    descKey: 'home.howItWorks.user.step1.description',
                                    icon: FileText
                                },
                                {
                                    step: '02',
                                    titleKey: 'home.howItWorks.user.step2.title',
                                    descKey: 'home.howItWorks.user.step2.description',
                                    icon: Cpu
                                },
                                {
                                    step: '03',
                                    titleKey: 'home.howItWorks.user.step3.title',
                                    descKey: 'home.howItWorks.user.step3.description',
                                    icon: MessageSquare
                                }
                            ].map((step, index) => (
                                <motion.div
                                    key={index}
                                    variants={itemVariants}
                                    className="relative"
                                >
                                    <div className="relative z-10 text-center">
                                        <div
                                            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary text-primary-content text-2xl font-bold mb-6 shadow-lg">
                                            {step.step}
                                        </div>
                                        <div className="inline-flex p-3 rounded-xl bg-base-100 mb-4 shadow-md">
                                            <step.icon className="text-primary" size={24}/>
                                        </div>
                                        <h3 className="text-2xl font-bold text-base-content mb-3">
                                            {t(step.titleKey)}
                                        </h3>
                                        <p className="text-base-content/70 leading-relaxed">
                                            {t(step.descKey)}
                                        </p>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    )}

                    {/* Admin Workflow */}
                    {isDepartmentAdmin && (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
                            {/* Connection lines for desktop */}
                            <div
                                className="hidden md:block absolute top-1/4 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-primary/30 to-transparent"/>

                            {[
                                {
                                    step: '01',
                                    titleKey: 'home.howItWorks.admin.step1.title',
                                    descKey: 'home.howItWorks.admin.step1.description',
                                    icon: Zap
                                },
                                {
                                    step: '02',
                                    titleKey: 'home.howItWorks.admin.step2.title',
                                    descKey: 'home.howItWorks.admin.step2.description',
                                    icon: TrendingUp
                                },
                                {
                                    step: '03',
                                    titleKey: 'home.howItWorks.admin.step3.title',
                                    descKey: 'home.howItWorks.admin.step3.description',
                                    icon: Cpu
                                }
                            ].map((step, index) => (
                                <motion.div
                                    key={index}
                                    variants={itemVariants}
                                    className="relative"
                                >
                                    <div className="relative z-10 text-center">
                                        <div
                                            className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-primary text-primary-content text-2xl font-bold mb-6 shadow-lg">
                                            {step.step}
                                        </div>
                                        <div className="inline-flex p-3 rounded-xl bg-base-100 mb-4 shadow-md">
                                            <step.icon className="text-primary" size={24}/>
                                        </div>
                                        <h3 className="text-2xl font-bold text-base-content mb-3">
                                            {t(step.titleKey)}
                                        </h3>
                                        <p className="text-base-content/70 leading-relaxed">
                                            {t(step.descKey)}
                                        </p>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    )}
                </div>
            </motion.section>
        </div>
    );
};
