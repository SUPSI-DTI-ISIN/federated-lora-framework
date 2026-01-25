import { motion } from 'framer-motion';
import { Plus, MessageSquare, ChevronRight, ChevronLeft } from 'lucide-react';
import { useTranslation } from "react-i18next";

interface ChatSidebarProps {
    isOpen: boolean;
    onToggle: () => void;
}

export const ChatSidebar = ({ isOpen, onToggle }: ChatSidebarProps) => {
    const { t } = useTranslation();

    return (
        <motion.aside
            initial={false}
            animate={{ width: isOpen ? 280 : 72 }}
            className="h-full bg-base-200/50 border-r border-base-content/5 flex flex-col items-center overflow-hidden transition-colors duration-300"
        >
            <div className="p-3 w-full flex flex-col items-center gap-4">
                <button
                    onClick={onToggle}
                    className="btn btn-ghost btn-sm w-full flex items-center justify-center hover:bg-base-300 rounded-xl"
                    title={isOpen ? t("chat.sidebar.collapse") : t("chat.sidebar.expand")}
                >
                    {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
                </button>

                {/* New Chat Button */}
                <button
                    className={`btn btn-primary shadow-lg shadow-primary/20 flex items-center transition-all duration-300 ${
                        isOpen ? "w-full justify-start px-4" : "w-12 h-12 p-0 justify-center rounded-2xl"
                    }`}
                >
                    <Plus size={20} className={isOpen ? "mr-2" : ""} />
                    {isOpen && <span className="truncate">Nuova chat</span>}
                </button>
            </div>

            {/* Chat History List */}
            <div className="flex-1 w-full overflow-y-auto overflow-x-hidden px-3 space-y-2 mt-4">
                {isOpen && (
                    <p className="px-2 pb-2 text-[10px] font-black text-base-content/30 uppercase tracking-[0.2em]">
                        Chat
                    </p>
                )}

                {/* Mock History Item */}
                <button className={`flex items-center gap-3 w-full p-3 rounded-xl transition-colors hover:bg-base-300 group ${
                    isOpen ? "" : "justify-center"
                }`}>
                    <MessageSquare size={18} className="shrink-0 opacity-50 group-hover:text-primary transition-colors" />
                    {isOpen && (
                        <span className="text-sm font-medium truncate opacity-80 group-hover:opacity-100">
                            Analisi dei dati v2
                        </span>
                    )}
                </button>
            </div>
        </motion.aside>
    );
};