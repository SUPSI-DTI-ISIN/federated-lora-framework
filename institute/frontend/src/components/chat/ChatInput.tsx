import { useRef, useEffect, type KeyboardEvent } from 'react';
import { useTranslation } from 'react-i18next';
import { Send, StopCircle, Paperclip } from 'lucide-react';

interface ChatInputProps {
    value: string;
    onChange: (value: string) => void;
    onSend: () => void;
    isLoading: boolean;
    onStop: () => void;
    enableAttach?: boolean;
}

export const ChatInput = ({
                              value,
                              onChange,
                              onSend,
                              isLoading,
                              onStop,
                              enableAttach = false,
                          }: ChatInputProps) => {
    const { t } = useTranslation();
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    useEffect(() => {
        const textarea = textareaRef.current;
        if (!textarea) return;

        textarea.style.height = 'auto';
        textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`;
    }, [value]);

    const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!isLoading && value.trim()) {
                onSend();
            }
        }
    };

    const canSend = value.trim().length > 0 && !isLoading;

    return (
        <div className="flex items-end gap-2">
            <div className="flex-1 relative">
        <textarea
            ref={textareaRef}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={t('chat.input.placeholder')}
            disabled={isLoading}
            rows={1}
            className="textarea textarea-bordered w-full resize-none min-h-13 pr-12"
        />

                {enableAttach && (
                    <button
                        type="button"
                        disabled={isLoading}
                        className="btn btn-ghost btn-sm btn-circle absolute right-2 bottom-2"
                        title={t('chat.input.attach')}
                    >
                        <Paperclip size={18} />
                    </button>
                )}
            </div>

            {/* Send / Stop */}
            {isLoading ? (
                <button
                    type="button"
                    onClick={onStop}
                    className="btn btn-error btn-circle"
                    title={t('chat.input.stop')}
                >
                    <StopCircle size={20} />
                </button>
            ) : (
                <button
                    type="button"
                    onClick={onSend}
                    disabled={!canSend}
                    className="btn btn-primary btn-circle"
                    title={t('chat.input.send')}
                >
                    <Send size={20} />
                </button>
            )}
        </div>
    );
};