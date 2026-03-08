import {useState} from "react";
import {Menu, Plus} from "lucide-react";
import {ChatSidebar} from "../components/chat/ChatSidebar";
import {getModelKey} from "../utils/envUtils.ts";
import {useGetAllChats} from "../hooks/institute/chat/useGetAllChats.ts";
import {ChatInterfaceWrapper} from "../components/chat/ChatInterfaceWrapper.tsx";
import {motion} from "framer-motion";
import {useReducedMotion} from "../hooks/useReducedMotion";
import {CreateChatModal} from "../components/chat/CreateChatModal.tsx";

export const ChatPage = () => {
    const modelKey = getModelKey();
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const {data: chats, isLoading: isLoadingChats, error: errorLoadingChats} = useGetAllChats();
    const [selectedChatId, setSelectedChatId] = useState<number | null>(null);
    const [showCreateModal, setShowCreateModal] = useState(false);
    const prefersReducedMotion = useReducedMotion();

    const handleChatCreated = (chatId: number) => {
        setSelectedChatId(chatId);
    };

    return (
        <>
            <motion.div
                initial={prefersReducedMotion ? {} : {opacity: 0, y: 12}}
                animate={prefersReducedMotion ? {} : {opacity: 1, y: 0}}
                transition={prefersReducedMotion ? {duration: 0} : {duration: 0.25}}
                className="flex h-[calc(100vh-4rem)] w-full overflow-hidden bg-base-100"
            >
                <ChatSidebar
                    isOpen={isSidebarOpen}
                    onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
                    chats={chats}
                    errorLoadingChats={errorLoadingChats}
                    isLoadingChats={isLoadingChats}
                    selectedChatId={selectedChatId}
                    onSelectChat={(chatId: number | null) => setSelectedChatId(chatId)}
                    onCreateChat={() => setShowCreateModal(true)}
                />


                <main className="flex flex-1 flex-col relative overflow-hidden w-full">
                    <header className="flex h-14 items-center justify-between border-b border-base-content/5 px-6 bg-base-100/50 backdrop-blur-md">
                        <div className="flex items-center gap-3">
                            {!isSidebarOpen && (
                                <button 
                                    onClick={() => setIsSidebarOpen(true)} 
                                    className="btn btn-ghost btn-sm btn-circle"
                                    aria-label="Open chat sidebar"
                                    aria-expanded={isSidebarOpen}
                                    aria-controls="chat-sidebar"
                                >
                                    <Menu size={18} />
                                </button>
                            )}
                            <h2 className="text-sm font-bold tracking-tight uppercase opacity-50">{modelKey}</h2>
                        </div>
                        
                        <button
                            onClick={() => setShowCreateModal(true)}
                            className="btn btn-primary btn-sm gap-2"
                        >
                            <Plus size={16} />
                            <span className="hidden sm:inline">New Chat</span>
                        </button>
                    </header>


                    <div className="flex-1 overflow-hidden w-full">
                        <ChatInterfaceWrapper modelKey={modelKey} chatId={selectedChatId} />
                    </div>
                </main>
            </motion.div>

            <CreateChatModal
                isOpen={showCreateModal}
                onClose={() => setShowCreateModal(false)}
                onChatCreated={handleChatCreated}
            />
        </>
    );
};
