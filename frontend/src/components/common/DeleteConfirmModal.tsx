import {useEffect} from 'react';
import {AlertTriangle} from 'lucide-react';
import {motion, AnimatePresence} from 'framer-motion';
import {useTranslation} from 'react-i18next';

interface DeleteConfirmModalProps {
    isOpen: boolean;
    onConfirm: () => void;
    onCancel: () => void;
    itemName?: string;
}

export const DeleteConfirmModal = ({
                                       isOpen,
                                       onConfirm,
                                       onCancel,
                                       itemName,
                                   }: DeleteConfirmModalProps) => {
    const {t} = useTranslation();

    useEffect(() => {
        const handleEscape = (event: KeyboardEvent) => {
            if (event.key === 'Escape' && isOpen) {
                onCancel();
            }
        };

        if (isOpen) {
            document.addEventListener('keydown', handleEscape);
            document.body.style.overflow = 'hidden';
        }

        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = 'unset';
        };
    }, [isOpen, onCancel]);

    return (
        <AnimatePresence>
            {isOpen && (
                <>
                    <motion.div
                        initial={{opacity: 0}}
                        animate={{opacity: 1}}
                        exit={{opacity: 0}}
                        transition={{duration: 0.2}}
                        className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
                        onClick={onCancel}
                        aria-hidden="true"
                    />

                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                        <motion.div
                            initial={{opacity: 0, scale: 0.95}}
                            animate={{opacity: 1, scale: 1}}
                            exit={{opacity: 0, scale: 0.95}}
                            transition={{duration: 0.2}}
                            className="modal-box relative max-w-md rounded-2xl bg-base-100 p-6 shadow-xl"
                            role="dialog"
                            aria-modal="true"
                            aria-labelledby="modal-title"
                            aria-describedby="modal-description"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="mb-4 flex justify-center">
                                <div className="rounded-full bg-error/10 p-3">
                                    <AlertTriangle
                                        size={32}
                                        className="text-error"
                                        strokeWidth={2}
                                        aria-hidden="true"
                                    />
                                </div>
                            </div>

                            <h3
                                id="modal-title"
                                className="mb-2 text-center text-xl font-semibold text-base-content"
                            >
                                {t('modal.delete.title')}
                            </h3>

                            <p
                                id="modal-description"
                                className="mb-6 text-center text-base-content/70"
                            >
                                {itemName
                                    ? t('modal.delete.messageNamed', {itemName})
                                    : t('modal.delete.message')}
                            </p>

                            <div className="flex gap-3">
                                <button
                                    onClick={onCancel}
                                    className="btn btn-ghost flex-1"
                                    type="button"
                                >
                                    {t('modal.delete.cancel')}
                                </button>
                                <button
                                    onClick={onConfirm}
                                    className="btn btn-error flex-1"
                                    type="button"
                                >
                                    {t('modal.delete.confirm')}
                                </button>
                            </div>
                        </motion.div>
                    </div>
                </>
            )}
        </AnimatePresence>
    );
}
