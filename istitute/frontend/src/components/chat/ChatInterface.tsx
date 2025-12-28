import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2 } from 'lucide-react';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { useInferenceModel } from '../../hooks/inference/useInferenceModel.ts';
import type {QueryResponseDTO} from "@isin/inference-service-client";

interface ChatInterfaceProps {
    initialPrompt: string;
}

export const ChatInterface = ({ initialPrompt }: ChatInterfaceProps) => {
    const { t } = useTranslation();

    const [inputValue, setInputValue] = useState('');
    const [userPrompt, setUserPrompt] = useState<string | null>(null);
    const [modelResponse, setModelResponse] = useState<QueryResponseDTO | null>(null);
    const [isQueryingModel, setIsQueryingModel] = useState(false);

    const messagesEndRef = useRef<HTMLDivElement>(null);

    const { mutateAsync: inferenceModel } = useInferenceModel();

    useEffect(() => {
        if (!initialPrompt) return;

        let isMounted = true;

        const runInitialInference = async () => {
            try {
                setIsQueryingModel(true);
                setUserPrompt(initialPrompt);
                setModelResponse(null);

                const response = await inferenceModel(initialPrompt);
                if (isMounted) {
                    setModelResponse(response);
                }
            } catch (error) {
                console.error('Initial inference error:', error);
            } finally {
                if (isMounted) {
                    setIsQueryingModel(false);
                }
            }
        };

        runInitialInference();

        return () => {
            isMounted = false;
        };
    }, [initialPrompt, inferenceModel]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [userPrompt, modelResponse, isQueryingModel]);

    const handleSendMessage = async () => {
        if (!inputValue.trim() || isQueryingModel) return;

        const prompt = inputValue.trim();
        setInputValue('');
        setUserPrompt(prompt);
        setModelResponse(null);

        try {
            setIsQueryingModel(true);
            const response = await inferenceModel(prompt);
            setModelResponse(response);
        } catch (error) {
            console.error('Error sending message:', error);
        } finally {
            setIsQueryingModel(false);
        }
    };

    const handleStopGeneration = () => {
        console.log('Stop generation requested');
    };

    return (
        <div className="h-full flex flex-col">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto px-4 py-6">
                <div className="max-w-4xl mx-auto space-y-6">
                    <AnimatePresence mode="popLayout">
                        {userPrompt && (
                            <ChatMessage
                                key="user"
                                message={{ role: 'user', content: userPrompt }}
                                index={0}
                            />
                        )}

                        {modelResponse && (
                            <ChatMessage
                                key="assistant"
                                message={{ role: 'assistant', content: modelResponse.response }}
                                index={1}
                            />
                        )}
                    </AnimatePresence>

                    {isQueryingModel && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="flex items-center gap-3 text-base-content/60"
                        >
                            <Loader2 className="animate-spin" size={20} />
                            <span>{t('chat.thinking')}</span>
                        </motion.div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <div className="border-t border-base-300 bg-base-200/50 backdrop-blur-sm">
                <div className="max-w-4xl mx-auto px-4 py-4">
                    <ChatInput
                        value={inputValue}
                        onChange={setInputValue}
                        onSend={handleSendMessage}
                        isLoading={isQueryingModel}
                        onStop={handleStopGeneration}
                    />

                    <p className="text-xs text-center text-base-content/50 mt-2">
                        {t('chat.disclaimer')}
                    </p>
                </div>
            </div>
        </div>
    );
};