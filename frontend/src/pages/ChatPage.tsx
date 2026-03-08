import {useState} from "react";
import {Menu} from "lucide-react";
import {ChatSidebar} from "../components/chat/ChatSidebar";
import {getModelKey} from "../utils/envUtils.ts";
import {useGetAllChats} from "../hooks/institute/chat/useGetAllChats.ts";
import {ChatInterfaceWrapper} from "../components/chat/ChatInterfaceWrapper.tsx";
import {motion} from "framer-motion";
import {useReducedMotion} from "../hooks/useReducedMotion";

export const ChatPage = () => {
    const modelKey = getModelKey();
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const {data: chats, isLoading: isLoadingChats, error: errorLoadingChats} = useGetAllChats();
    const [selectedChatId, setSelectedChatId] = useState<number | null>(null);
    const prefersReducedMotion = useReducedMotion();

    return (
        <motion.div
            initial={prefersReducedMotion ? {} : {opacity: 0, y: 12}}
            animate={prefersReducedMotion ? {} : {opacity: 1, y: 0}}
            transition={prefersReducedMotion ? {duration: 0} : {duration: 0.25}}
            className="flex h-[calc(100vh-4rem)] overflow-hidden bg-base-100"
        >
            <ChatSidebar
                isOpen={isSidebarOpen}
                onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
                chats={chats}
                errorLoadingChats={errorLoadingChats}
                isLoadingChats={isLoadingChats}
                selectedChatId={selectedChatId}
                onSelectChat={(chatId: number | null) => setSelectedChatId(chatId)}
            />


            <main className="flex flex-1 flex-col relative overflow-hidden">
                <header className="flex h-14 items-center justify-between border-b border-base-content/5 px-6 bg-base-100/50 backdrop-blur-md">
                    <div className="flex items-center gap-3">
                        {!isSidebarOpen && (
                            <button 
                                onClick={() => setIsSidebarOpen(true)} 
                                className="btn btn-ghost btn-xs"
                                aria-label="Open chat sidebar"
                                aria-expanded={isSidebarOpen}
                                aria-controls="chat-sidebar"
                            >
                                <Menu size={18} />
                            </button>
                        )}
                        <h2 className="text-sm font-bold tracking-tight uppercase opacity-50">{modelKey}</h2>
                    </div>
                </header>


                <div className="flex-1 overflow-hidden">
                    <ChatInterfaceWrapper modelKey={modelKey} chatId={selectedChatId} />
                </div>
            </main>
        </motion.div>
    );
};