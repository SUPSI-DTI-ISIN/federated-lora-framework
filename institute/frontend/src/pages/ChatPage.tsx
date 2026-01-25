import {useState} from "react";
import {motion} from "framer-motion";
import {Sparkles} from "lucide-react";
import {useTranslation} from "react-i18next";

import {ChatInterface} from "../components/chat/ChatInterface";
import {ChatSidebar} from "../components/chat/ChatSidebar";
import {getModelKey} from "../utils/envUtils.ts";

export const ChatPage = () => {
    const {t} = useTranslation();
    const modelKey = getModelKey();
    const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(true);

    return (
        <div className="h-[calc(100vh-6.5rem)] bg-linear-to-br from-base-100 via-base-200 to-base-100">
            <div className="h-full max-w-6xl mx-auto flex">
                {/* Sidebar */}
                <ChatSidebar isOpen={isSidebarOpen} onToggle={() => setIsSidebarOpen((s) => !s)}/>

                <div className="flex-1 flex flex-col">
                    {/* Header */}
                    <motion.div
                        initial={{opacity: 0, y: -12}}
                        animate={{opacity: 1, y: 0}}
                        className="bg-base-200/80 backdrop-blur-sm border-b border-base-300 px-6 py-4"
                    >
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <div
                                    className="w-10 h-10 rounded-lg bg-linear-to-br from-primary to-secondary flex items-center justify-center">
                                    <Sparkles className="text-primary-content" size={18}/>
                                </div>
                                <div>
                                    <h1 className="text-xl font-bold">{t("chat.title")}</h1>
                                    <p className="text-sm text-base-content/60">{t("chat.subtitle")}</p>
                                </div>
                            </div>
                        </div>
                    </motion.div>

                    {/* Main */}
                    <div className="flex-1 overflow-hidden">
                        <ChatInterface modelKey={modelKey}/>
                    </div>
                </div>
            </div>
        </div>
    );
};