import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import { User, Sparkles, Copy, Check } from 'lucide-react';
import { useState } from 'react';
import toast from 'react-hot-toast';

interface ChatMessage {
    role: 'user' | 'assistant';
    content: string;
}

interface ChatMessageProps {
    message: ChatMessage;
    index: number;
}

export const ChatMessage = ({ message, index }: ChatMessageProps) => {
    const { t } = useTranslation();
    const [copied, setCopied] = useState(false);
    const isUser = message.role === 'user';

    const handleCopy = async () => {
        try {
            await navigator.clipboard.writeText(message.content);
            setCopied(true);
            toast.success(t('chat.message.copied'));
            setTimeout(() => setCopied(false), 2000);
        } catch (error) {
            toast.error(t('chat.message.copyError'));
        }
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ delay: index * 0.05 }}
            className={`flex gap-4 ${isUser ? 'justify-end' : 'justify-start'}`}
        >
            <div className={`flex gap-3 max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                {/* Avatar */}
                <div className="shrink-0">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                        isUser
                            ? 'bg-primary text-primary-content'
                            : 'bg-linear-to-br from-secondary to-accent text-secondary-content'
                    }`}>
                        {isUser ? <User size={20} /> : <Sparkles size={20} />}
                    </div>
                </div>

                {/* Message Content */}
                <div className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
                    <div className={`rounded-2xl px-4 py-3 ${
                        isUser
                            ? 'bg-primary text-primary-content rounded-tr-sm'
                            : 'bg-base-200 text-base-content rounded-tl-sm'
                    }`}>
                        <p className="whitespace-pre-wrap wrap-break-word">{message.content}</p>
                    </div>

                    {/* Message Footer */}
                    <div className={`flex items-center gap-2 mt-1 px-2 ${
                        isUser ? 'flex-row-reverse' : 'flex-row'
                    }`}>
                        {!isUser && (
                            <button
                                onClick={handleCopy}
                                className="btn btn-ghost btn-xs gap-1 opacity-0 group-hover:opacity-100 transition-opacity"
                                title={t('chat.message.copy')}
                            >
                                {copied ? (
                                    <Check size={14} className="text-success" />
                                ) : (
                                    <Copy size={14} />
                                )}
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </motion.div>
    );
};