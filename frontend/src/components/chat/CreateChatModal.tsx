import { useState } from "react";
import { MessageSquare, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import { useCreateChat } from "../../hooks/institute/chat/useCreateChat.ts";
import toast from "react-hot-toast";

interface CreateChatModalProps {
    isOpen: boolean;
    onClose: () => void;
    onChatCreated: (chatId: number) => void;
}

export const CreateChatModal = ({ isOpen, onClose, onChatCreated }: CreateChatModalProps) => {
    const { t } = useTranslation();
    const [title, setTitle] = useState("");
    const { mutateAsync: createChat, isPending: isCreating } = useCreateChat();

    const handleCreate = async () => {
        if (!title.trim()) return;
        
        try {
            const newChat = await createChat({ title: title.trim() });
            toast.success(t("chat.createSuccess"));
            setTitle("");
            onChatCreated(newChat.id);
            onClose();
        } catch (e) {
            console.error(e);
            toast.error(t("chat.errorCreate"));
        }
    };

    const handleClose = () => {
        setTitle("");
        onClose();
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <div className="modal modal-open backdrop-blur-sm bg-base-content/20">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.9 }}
                        className="modal-box border border-base-content/10 p-0"
                    >
                        <div className="p-6 border-b border-base-content/5 flex justify-between items-center bg-base-200/50">
                            <h3 className="text-xl font-bold flex items-center gap-2">
                                <MessageSquare className="text-primary" size={22} />
                                {t("chat.modal.title")}
                            </h3>
                        </div>

                        <div className="p-6 space-y-4">
                            <div className="form-control">
                                <label className="label">
                                    <span className="label-text text-xs font-bold uppercase text-base-content/50">
                                        {t("chat.modal.nameLabel")}
                                    </span>
                                </label>
                                <input
                                    className="input input-bordered focus:input-primary transition-all bg-base-100"
                                    placeholder={t("chat.modal.namePlaceholder")}
                                    value={title}
                                    onChange={(e) => setTitle(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === "Enter" && title.trim() && !isCreating) {
                                            handleCreate();
                                        }
                                    }}
                                    autoFocus
                                />
                            </div>
                        </div>

                        <div className="p-6 bg-base-200/30 flex gap-3">
                            <button
                                className="btn btn-ghost flex-1"
                                onClick={handleClose}
                                disabled={isCreating}
                            >
                                {t("common.cancel")}
                            </button>
                            <button
                                className="btn btn-primary flex-1 shadow-lg shadow-primary/20"
                                onClick={handleCreate}
                                disabled={isCreating || !title.trim()}
                            >
                                {isCreating ? (
                                    <Loader2 className="animate-spin" size={18} />
                                ) : (
                                    t("chat.modal.create")
                                )}
                            </button>
                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
};
