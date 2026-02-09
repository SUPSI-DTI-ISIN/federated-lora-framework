import {motion} from 'framer-motion';
import {Plus, MessageSquare, ChevronRight, ChevronLeft} from 'lucide-react';
import {useTranslation} from "react-i18next";
import type {ChatDTO} from "@isin/chat-service-client";
import {useCreateChat} from "../../hooks/chat/useCreateChat.ts";
import {useDeleteChat} from "../../hooks/chat/useDeleteChat.ts";
import {useState} from "react";
import toast from "react-hot-toast";

interface ChatSidebarProps {
    isOpen: boolean;
    onToggle: () => void;
    chats?: ChatDTO[];
    errorLoadingChats: Error | null;
    isLoadingChats?: boolean;
    selectedChatId?: number | null;
    onSelectChat: (chatId: number | null) => void;
}

export const ChatSidebar = ({
                                isOpen,
                                onToggle,
                                chats,
                                errorLoadingChats,
                                isLoadingChats,
                                selectedChatId,
                                onSelectChat
                            }: ChatSidebarProps) => {
    const {t} = useTranslation();

    const {mutateAsync: createChat} = useCreateChat();
    const {mutateAsync: deleteChat} = useDeleteChat();

    const [creating, setCreating] = useState<boolean>(false);
    //const [deleting, setDeleting] = useState<boolean>(false);

    const [deletingId, setDeletingId] = useState<number | null>(null);

    const handleCreate = async () => {
        const title = window.prompt(t("chat.sidebar.newChatPrompt") ?? "Titolo chat");
        if (title === null) return;

        setCreating(true);
        try {
            const newChat = await createChat({title: title.trim() || null});
            onSelectChat(newChat.id);
        } catch (err) {
            console.error(err);
            toast.error(t("chat.errorCreate") ?? "Errore nella creazione della chat");
        } finally {
            setCreating(false);
        }
    };

    const handleDelete = async (chatId: number) => {
        if (!window.confirm(t("chat.sidebar.confirmDelete") ?? "Eliminare questa chat?")) return;
        //setDeleting(true);
        setDeletingId(chatId);
        try {
            await deleteChat(chatId);
            if (selectedChatId === chatId) onSelectChat(null);
        } catch (err) {
            console.error(err);
            toast.error(t("chat.errorDelete") ?? "Errore nell'eliminazione della chat");
        } finally {
            //setDeleting(false);
            setDeletingId(null);
        }
    };

    return (
        <motion.aside
            initial={false}
            animate={{width: isOpen ? 280 : 72}}
            className="h-full bg-base-200/50 border-r border-base-content/5 flex flex-col items-center overflow-hidden transition-colors duration-300"
        >
            <div className="p-3 w-full flex flex-col items-center gap-4">
                <button
                    onClick={onToggle}
                    className="btn btn-ghost btn-sm w-full flex items-center justify-center hover:bg-base-300 rounded-xl"
                    title={isOpen ? t("chat.sidebar.collapse") : t("chat.sidebar.expand")}
                >
                    {isOpen ? <ChevronLeft size={20}/> : <ChevronRight size={20}/>}
                </button>


                {/* New Chat Button */}
                <button
                    onClick={handleCreate}
                    className={`btn btn-primary shadow-lg shadow-primary/20 flex items-center transition-all duration-300 w-full justify-start`}
                    disabled={creating}
                >
                    <Plus size={20} />
                    {isOpen && <span
                        className="truncate">{creating ? (t("chat.sidebar.creating") ?? "Creando...") : t("chat.sidebar.newChat") ?? "Nuova chat"}</span>}
                </button>
            </div>

            <div className="flex-1 w-full overflow-y-auto overflow-x-hidden px-3 space-y-2 mt-4">
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
                    chats.map((chat) => (
                        <div key={chat.id} className="flex items-center gap-3 w-full">
                            <button
                                onClick={() => onSelectChat(chat.id)}
                                className={`flex items-center gap-3 w-full p-3 rounded-xl transition-colors group ${isOpen ? "justify-start" : "justify-center"} ${selectedChatId === chat.id ? "bg-base-100 border border-primary" : "hover:bg-base-300"}`}
                            >
                                <MessageSquare size={18}
                                               className="shrink-0 opacity-50 group-hover:text-primary transition-colors"/>
                                <div className="flex-1 flex items-center justify-between">
                                    <span
                                        className="text-sm font-medium truncate opacity-80 group-hover:opacity-100">{chat.title ?? `Chat #${chat.id}`}</span>
                                    <span
                                        className="text-xs opacity-40 ml-2">{new Date(chat.created_at).toLocaleDateString()}</span>
                                </div>
                            </button>


                            {/* Delete button visible when sidebar expanded */}
                            <button
                                onClick={() => handleDelete(chat.id)}
                                className={`btn btn-ghost btn-xs ml-2 ${deletingId === chat.id ? "loading" : ""}`}
                                title={t("chat.sidebar.delete") ?? "Elimina"}
                            >
                                {deletingId === chat.id ? "" : "🗑"}
                            </button>
                        </div>
                    ))
                )}
            </div>
        </motion.aside>
    );
};