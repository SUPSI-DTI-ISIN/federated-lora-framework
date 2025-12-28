import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { Sparkles, FileText, Edit, Lightbulb, Zap } from 'lucide-react';

interface WelcomeScreenProps {
    onStartChat: (prompt: string) => void;
}

export const WelcomeScreen = ({ onStartChat }: WelcomeScreenProps) => {
    const { t } = useTranslation();

    const suggestions = [
        {
            icon: FileText,
            title: 'chat.welcome.suggestions.create.title',
            description: 'chat.welcome.suggestions.create.description',
            prompt: 'chat.welcome.suggestions.create.prompt'
        },
        {
            icon: Edit,
            title: 'chat.welcome.suggestions.improve.title',
            description: 'chat.welcome.suggestions.improve.description',
            prompt: 'chat.welcome.suggestions.improve.prompt'
        },
        {
            icon: Lightbulb,
            title: 'chat.welcome.suggestions.review.title',
            description: 'chat.welcome.suggestions.review.description',
            prompt: 'chat.welcome.suggestions.review.prompt'
        },
        {
            icon: Zap,
            title: 'chat.welcome.suggestions.structure.title',
            description: 'chat.welcome.suggestions.structure.description',
            prompt: 'chat.welcome.suggestions.structure.prompt'
        },
    ];

    const handleSuggestionClick = (prompt: string) => {
        onStartChat(prompt);
    };

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
        <div className="h-full flex items-center justify-center p-8">
            <div className="max-w-4xl w-full">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-center mb-12"
                >
                    <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-linear-to-br from-primary to-secondary mb-6">
                        <Sparkles className="text-primary-content" size={40} />
                    </div>

                    <h1 className="text-4xl font-bold mb-4">
                        {t('chat.welcome.title')}
                    </h1>

                    <p className="text-xl text-base-content/70 max-w-2xl mx-auto">
                        {t('chat.welcome.subtitle')}
                    </p>
                </motion.div>

                <motion.div
                    variants={containerVariants}
                    initial="hidden"
                    animate="visible"
                    className="grid grid-cols-1 md:grid-cols-2 gap-4"
                >
                    {suggestions.map((suggestion, index) => {
                        const Icon = suggestion.icon;
                        return (
                            <motion.button
                                key={index}
                                variants={itemVariants}
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                                onClick={() => handleSuggestionClick(t(suggestion.prompt))}
                                className="card bg-base-100 shadow-lg hover:shadow-xl transition-all text-left"
                            >
                                <div className="card-body">
                                    <div className="flex items-start gap-4">
                                        <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center shrink-0">
                                            <Icon className="text-primary" size={24} />
                                        </div>
                                        <div className="flex-1">
                                            <h3 className="font-semibold text-lg mb-2">
                                                {t(suggestion.title)}
                                            </h3>
                                            <p className="text-sm text-base-content/70">
                                                {t(suggestion.description)}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </motion.button>
                        );
                    })}
                </motion.div>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.6 }}
                    className="mt-12 text-center"
                >
                    <p className="text-sm text-base-content/50">
                        {t('chat.welcome.hint')}
                    </p>
                </motion.div>
            </div>
        </div>
    );
};