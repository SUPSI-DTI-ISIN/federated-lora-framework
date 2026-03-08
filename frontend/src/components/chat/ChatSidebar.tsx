import {motion} from 'framer-motion';
import {Plus, MessageSquare, ChevronRight, ChevronLeft, Trash2} from 'lucide-react';
import {useTranslation} from "react-i18next";
import type {ChatDTO} from "@isin/chat-service-client";
import {useDeleteChat} from "../../hooks/institute/chat/useDeleteChat.ts";
import {useState} from "react";
import toast from "react-hot-toast";
import {DeleteConfirmModal} from "../common/DeleteConfirmModal";
import {useReducedMotion} from "../../hooks/useReducedMotion";

interface ChatSidebarProps {
    isOpen: boolean;
    onToggle: () => void;
    chats?: ChatDTO[];
    errorLoadingChats: Error | null;
    isLoadingChats?: boolean;
    selectedChatId?: number | null;
    onSelectChat: (chatId: number | null) => void;
    onCreateChat: () => void;
}

export const ChatSidebar = ({
                                isOpen,
                                onToggle,
                                chats,
                                errorLoadingChats,
                                isLoadingChats,
                                selectedChatId,
                                onSelectChat,
                                onCreateChat
                            }: ChatSidebarProps) => {
    const {t} = useTranslation();
    const prefersReducedMotion = useReducedMotion();

    const {mutateAsync: deleteChat} = useDeleteChat();

    const [deletingId, setDeletingId] = useState<number | null>(null);
    const [deleteModalOpen, setDeleteModalOpen] = useState<boolean>(false);
    const [chatToDelete, setChatToDelete] = useState<ChatDTO | null>(null);

    const handleDeleteClick = (chat: ChatDTO) => {
        setChatToDelete(chat);
        setDeleteModalOpen(true);
    };

    const handleDeleteConfirm = async () => {
        if (!chatToDelete) return;
        
        setDeletingId(chatToDelete.id);
        setDeleteModalOpen(false);
        
        try {
            await deleteChat(chatToDelete.id);
            if (selectedChatId === chatToDelete.id) onSelectChat(null);
            toast.success(t("chat.deleteSuccess") ?? "Chat deleted successfully");
        } catch (err) {
            console.error(err);
            toast.error(t("chat.errorDelete") ?? "Error deleting chat");
        } finally {
            setDeletingId(null);
            setChatToDelete(null);
        }
    };

    const handleDeleteCancel = () => {
        setDeleteModalOpen(false);
        setChatToDelete(null);
    };

    return (
        <>
            <motion.aside
                id="chat-sidebar"
                initial={false}
                animate={{width: isOpen ? 280 : 72}}
                className="h-full bg-base-200/50 border-r border-base-content/5 flex flex-col items-center overflow-hidden transition-colors duration-300"
            >
                <div className="p-3 w-full flex flex-col items-center gap-4">
                    <button
                        onClick={onToggle}
                        className="btn btn-ghost btn-sm w-full flex items-center justify-center hover:bg-base-300 rounded-xl"
                        aria-label={isOpen ? t("chat.sidebar.collapse") : t("chat.sidebar.expand")}
                        aria-expanded={isOpen}
                        aria-controls="chat-list"
                    >
                        {isOpen ? <ChevronLeft size={20}/> : <ChevronRight size={20}/>}
                    </button>


                {/* New Chat Button */}
                <button
                    onClick={onCreateChat}
                    className={`btn btn-primary shadow-lg shadow-primary/20 flex items-center transition-all duration-300 w-full justify-start`}
                    aria-label={t("chat.sidebar.newChat") ?? "New chat"}
                >
                    <Plus size={20} />
                    {isOpen && <span className="truncate">{t("chat.sidebar.newChat") ?? "New chat"}</span>}
                </button>
            </div>

            <div id="chat-list" className="flex-1 w-full overflow-y-auto overflow-x-hidden px-3 space-y-2 mt-4">
                {isOpen && (
                    <p className="px-2 pb-2 text-[10px] font-black text-base-content/30 uppercase tracking-[0.2em]">Chats</p>
                )}

                {/* Loading skeletons */}
                {isLoadingChats && (
                    <div className="space-y-2 px-2">
                        {Array.from({length: 6}).map((_, i) => (
                            <div key={i}
                                 className={`h-12 rounded-xl ${isOpen ? "px-3 py-2" : "w-12 h-12 mx-auto"} bg-base-300 animate-pulse`}/>
                        ))}
                    </div>
                )}

                {!isLoadingChats && (!chats || chats.length === 0) && (
                    <div className="px-3">
                        <p className="text-sm opacity-40">{t("chat.sidebar.noChats") ?? "Nessuna chat ancora. Crea la prima!"}</p>
                    </div>
                )}

                {errorLoadingChats && (
                    <div className="card bg-base-100 shadow p-4 text-red-600">
                        <div>{t("chats.errorFetch")}</div>
                    </div>
                )}

                {/* Real chats */}
                {isOpen && !isLoadingChats && chats && chats.length > 0 && (
                    <motion.div
                        initial="hidden"
                        animate="visible"
                        variants={prefersReducedMotion ? {} : {
                            visible: {
                                transition: {
                                    staggerChildren: 0.05
                                }
                            }
                        }}
                    >
                        {chats.map((chat) => (
                            <motion.div
                                key={chat.id}
                                variants={prefersReducedMotion ? {} : {
                                    hidden: { opacity: 0, y: 8 },
                                    visible: { opacity: 1, y: 0 }
                                }}
                                className="flex items-center gap-2 w-full"
                            >
                                <button
                                    onClick={() => onSelectChat(chat.id)}
                                    className={`flex items-center gap-3 flex-1 p-3 rounded-xl transition-colors group ${isOpen ? "justify-start" : "justify-center"} ${selectedChatId === chat.id ? "bg-base-100 border border-primary" : "hover:bg-base-300"}`}
                                    aria-label={`Select chat: ${chat.title ?? `Chat #${chat.id}`}`}
                                    aria-current={selectedChatId === chat.id ? "true" : undefined}
                                >
                                    <MessageSquare size={18}
                                                   className="shrink-0 opacity-50 group-hover:text-primary transition-colors"/>
                                    <div className="flex-1 flex items-center justify-between min-w-0">
                                        <span
                                            className="text-sm font-medium truncate opacity-80 group-hover:opacity-100">{chat.title ?? `Chat #${chat.id}`}</span>
                                        <span
                                            className="text-xs opacity-40 ml-2 flex-shrink-0">{new Date(chat.created_at).toLocaleDateString()}</span>
                                    </div>
                                </button>

                                {/* Delete button visible when sidebar expanded */}
                                <button
                                    onClick={() => handleDeleteClick(chat)}
                                    className="btn btn-ghost btn-sm min-h-[44px] min-w-[44px] p-2"
                                    disabled={deletingId === chat.id}
                                    aria-label={`Delete chat: ${chat.title ?? `Chat #${chat.id}`}`}
                                >
                                    {deletingId === chat.id ? (
                                        <span className="loading loading-spinner loading-xs"></span>
                                    ) : (
                                        <Trash2 size={16} />
                                    )}
                                </button>
                            </motion.div>
                        ))}
                    </motion.div>
                )}
            </div>
        </motion.aside>

        <DeleteConfirmModal
            isOpen={deleteModalOpen}
            onConfirm={handleDeleteConfirm}
            onCancel={handleDeleteCancel}
            itemName={chatToDelete?.title ?? `Chat #${chatToDelete?.id}`}
        />
        </>
    );
};