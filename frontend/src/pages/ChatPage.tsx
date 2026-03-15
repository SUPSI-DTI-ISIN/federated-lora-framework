import {useState, useMemo} from "react";
import {MessageSquare, Plus, Trash2} from "lucide-react";
import {getModelKey} from "../utils/envUtils.ts";
import {useGetAllChats} from "../hooks/institute/chat/useGetAllChats.ts";
import {motion, AnimatePresence} from "framer-motion";
import {useReducedMotion} from "../hooks/useReducedMotion";
import {CreateChatModal} from "../components/chat/CreateChatModal.tsx";
import {useTranslation} from "react-i18next";
import {ChatInterface} from "../components/chat/ChatInterface.tsx";
import {EmptyChatState} from "../components/chat/EmptyChatState.tsx";
import {useDeleteChat} from "../hooks/institute/chat/useDeleteChat.ts";
import {DeleteConfirmModal} from "../components/common/DeleteConfirmModal.tsx";
import toast from "react-hot-toast";
import type {ChatDTO} from "@isin/chat-service-client";
import {useChatSse} from "../hooks/institute/chat/useChatSse.ts";

export const ChatPage = () => {
    useChatSse();
    const {t} = useTranslation();
    const modelKey = getModelKey();
    const {data: chats, isLoading: isLoadingChats} = useGetAllChats();
    const [selectedChatId, setSelectedChatId] = useState<number | null>(null);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [chatToDelete, setChatToDelete] = useState<ChatDTO | null>(null);
    const prefersReducedMotion = useReducedMotion();

    const {mutateAsync: deleteChat} = useDeleteChat();
    const [isDeleting, setIsDeleting] = useState(false);

    const handleChatCreated = (chatId: number) => {
        setSelectedChatId(chatId);
    };

    const handleDeleteClick = (chat: ChatDTO, e: React.MouseEvent) => {
        e.stopPropagation();
        setChatToDelete(chat);
        setShowDeleteModal(true);
    };

    const handleDeleteConfirm = async () => {
        if (!chatToDelete) return;

        setIsDeleting(true);
        setShowDeleteModal(false);

        try {
            await deleteChat(chatToDelete.id);
            if (selectedChatId === chatToDelete.id) setSelectedChatId(null);
            toast.success(t("chat.deleteSuccess"));
        } catch (err) {
            console.error(err);
            toast.error(t("chat.errorDelete"));
        } finally {
            setIsDeleting(false);
            setChatToDelete(null);
        }
    };

    const sortedChats = useMemo(() => {
        if (!chats) return [];
        return [...chats].sort((a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
    }, [chats]);

    return (
        <>
            <motion.div
                initial={prefersReducedMotion ? {} : {opacity: 0, y: 12}}
                animate={prefersReducedMotion ? {} : {opacity: 1, y: 0}}
                transition={prefersReducedMotion ? {duration: 0} : {duration: 0.25}}
                className="flex h-[calc(100vh-4rem)] w-full overflow-hidden bg-base-100"
            >
                {/* Left Sidebar - Chat History */}
                <aside className="w-80 border-r border-base-content/5 flex flex-col bg-base-100">
                    {/* Header */}
                    <div className="p-6 border-b border-base-content/5">
                        <button
                            onClick={() => setShowCreateModal(true)}
                            className="btn btn-primary w-full gap-2 shadow-lg"
                        >
                            <Plus size={20}/>
                            {t("chat.sidebar.newChat")}
                        </button>
                    </div>

                    {/* Chat List */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-2">
                        {isLoadingChats ? (
                            <div className="space-y-2">
                                {Array.from({length: 5}).map((_, i) => (
                                    <div key={i} className="h-16 bg-base-200 rounded-xl animate-pulse"/>
                                ))}
                            </div>
                        ) : sortedChats.length === 0 ? (
                            <div className="text-center py-12">
                                <MessageSquare size={48} className="mx-auto text-base-content/20 mb-4"/>
                                <p className="text-sm text-base-content/60">{t("chat.sidebar.noChats")}</p>
                            </div>
                        ) : (
                            <AnimatePresence>
                                {sortedChats.map((chat) => (
                                    <motion.div
                                        key={chat.id}
                                        initial={{opacity: 0, x: -20}}
                                        animate={{opacity: 1, x: 0}}
                                        exit={{opacity: 0, x: -20}}
                                        className={`group relative p-4 rounded-xl cursor-pointer transition-all ${
                                            selectedChatId === chat.id
                                                ? 'bg-primary text-primary-content shadow-lg'
                                                : 'hover:bg-base-200'
                                        }`}
                                        onClick={() => setSelectedChatId(chat.id)}
                                    >
                                        <div className="flex items-start justify-between gap-2">
                                            <div className="flex-1 min-w-0">
                                                <h3 className={`font-semibold truncate ${
                                                    selectedChatId === chat.id ? 'text-primary-content' : 'text-base-content'
                                                }`}>
                                                    {chat.title || `Chat #${chat.id}`}
                                                </h3>
                                                <p className={`text-xs mt-1 ${
                                                    selectedChatId === chat.id ? 'text-primary-content/70' : 'text-base-content/50'
                                                }`}>
                                                    {new Date(chat.created_at).toLocaleDateString()}
                                                </p>
                                            </div>
                                            {chat.is_doing_inference && (
                                                <span className={`loading loading-spinner loading-xs shrink-0 mt-1 ${
                                                    selectedChatId === chat.id ? 'text-primary-content' : 'text-primary'
                                                }`} aria-label="Inference in progress"/>
                                            )}
                                            <button
                                                onClick={(e) => handleDeleteClick(chat, e)}
                                                disabled={isDeleting}
                                                className={`btn btn-ghost btn-xs btn-circle opacity-0 group-hover:opacity-100 transition-opacity ${
                                                    selectedChatId === chat.id ? 'text-primary-content hover:bg-primary-content/20' : 'text-error hover:bg-error/10'
                                                }`}
                                            >
                                                {isDeleting && chatToDelete?.id === chat.id ? (
                                                    <span className="loading loading-spinner loading-xs"/>
                                                ) : (
                                                    <Trash2 size={14}/>
                                                )}
                                            </button>
                                        </div>
                                    </motion.div>
                                ))}
                            </AnimatePresence>
                        )}
                    </div>

                    {/* Footer Info */}
                    <div className="p-4 border-t border-base-content/5">
                        <div className="text-xs text-base-content/40 text-center">
                            <span className="font-mono">{modelKey}</span>
                        </div>
                    </div>
                </aside>

                {/* Main Chat Area */}
                <main className="flex-1 flex flex-col overflow-hidden">
                    {selectedChatId ? (
                        <ChatInterface
                            modelKey={modelKey}
                            chatId={selectedChatId}
                            isDoingInference={chats?.find(c => c.id === selectedChatId)?.is_doing_inference ?? false}
                        />
                    ) : (
                        <EmptyChatState/>
                    )}
                </main>
            </motion.div>

            <CreateChatModal
                isOpen={showCreateModal}
                onClose={() => setShowCreateModal(false)}
                onChatCreated={handleChatCreated}
            />

            <DeleteConfirmModal
                isOpen={showDeleteModal}
                onConfirm={handleDeleteConfirm}
                onCancel={() => setShowDeleteModal(false)}
                itemName={chatToDelete?.title || `Chat #${chatToDelete?.id}`}
            />
        </>
    );
};
