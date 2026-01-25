import {useState} from "react";
import {Menu} from "lucide-react";

import {ChatInterface} from "../components/chat/ChatInterface";
import {ChatSidebar} from "../components/chat/ChatSidebar";
import {getModelKey} from "../utils/envUtils.ts";

export const ChatPage = () => {
    // const { t } = useTranslation();
    const modelKey = getModelKey();
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    return (
        <div className="flex h-[calc(100vh-4rem)] overflow-hidden bg-base-100">
            <ChatSidebar
                isOpen={isSidebarOpen}
                onToggle={() => setIsSidebarOpen(!isSidebarOpen)}
            />

            <main className="flex flex-1 flex-col relative overflow-hidden">
                <header className="flex h-14 items-center justify-between border-b border-base-content/5 px-6 bg-base-100/50 backdrop-blur-md">
                    <div className="flex items-center gap-3">
                        {!isSidebarOpen && (
                            <button onClick={() => setIsSidebarOpen(true)} className="btn btn-ghost btn-xs">
                                <Menu size={18} />
                            </button>
                        )}
                        <h2 className="text-sm font-bold tracking-tight uppercase opacity-50">
                            {modelKey}
                        </h2>
                    </div>
                </header>

                <div className="flex-1 overflow-hidden">
                    <ChatInterface modelKey={modelKey} />
                </div>
            </main>
        </div>
    );
};