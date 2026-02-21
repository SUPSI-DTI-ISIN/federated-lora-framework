import {useMemo, useRef, useState} from "react";
import {useTranslation} from "react-i18next";
import toast from "react-hot-toast";
import {ChatComposer} from "./ChatComposer";
import {useInferenceModel} from "../../hooks/institute/chat/useInferenceModel.ts";
import {Cpu, Sparkles, User} from "lucide-react";
import {useGetAllMessagesByChat} from "../../hooks/institute/chat/useGetAllMessagesByChat.ts";


interface ChatInterfaceProps {
    modelKey: string;
    chatId: number;
}

export const ChatInterface = ({
                                  modelKey,
                                  chatId
                              }: ChatInterfaceProps) => {

    const {t} = useTranslation();
    const { data: messages, isLoading: isLoadingMessages, error: errorLoadingMessages } = useGetAllMessagesByChat(chatId);

    const scrollRef = useRef<HTMLDivElement | null>(null);

    const [isRunningInference, setIsRunningInference] = useState<boolean>(false);
    const {mutateAsync: runInference} = useInferenceModel();

    const sortedMessages = useMemo(() => {
        if (!messages) return [];
        return [...messages].sort(
            (msg1, msg2) =>
                new Date(msg1.created_at).getTime() -
                new Date(msg2.created_at).getTime()
        );
    }, [messages]);

    const handleSend = async (prompt: string, adapterVersion?: number | null) => {
        if (isRunningInference) return;
        setIsRunningInference(true);
        try {
            await runInference({
                chatId: chatId,
                modelKey: modelKey,
                adapterVersion: adapterVersion ?? null,
                prompt: prompt
            });
        } catch (err: any) {
            console.error(err);
            toast.error(t("chat.errorInference") ?? "Errore inferenza");
        } finally {
            setIsRunningInference(false);
        }
    };

    if(!messages || errorLoadingMessages){
        return (
            <div className="card bg-base-100 shadow p-4 text-red-600">
                <div>{t("messages.errorFetch")}</div>
            </div>
        )
    }

    return (
        <div className="h-full flex flex-col max-w-4xl mx-auto w-full">
            <div className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-8 scroll-smooth" ref={scrollRef}>
                {isLoadingMessages && (
                    <div className="space-y-4">
                        {Array.from({ length: 5 }).map((_, i) => (
                            <div key={i} className="flex gap-4 items-start">
                                <div className="h-8 w-8 rounded-full bg-base-300 animate-pulse" />
                                <div className="flex-1">
                                    <div className="h-4 rounded-md bg-base-300 w-3/4 mb-2 animate-pulse" />
                                    <div className="h-4 rounded-md bg-base-300 w-1/2 animate-pulse" />
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {sortedMessages && sortedMessages.map((message) => {
                    const from = message.role === "user" ? "user" : "assistant";
                    return (
                        <div key={message.id} className={`flex gap-4 ${from === "user" ? "flex-row-reverse" : ""}`}>
                            <div className={`h-8 w-8 rounded-full flex items-center justify-center shrink-0 ${from === "user" ? "bg-primary text-primary-content" : "bg-secondary text-secondary-content"}`}>
                                {from === "user" ? <User size={16} /> : <Sparkles size={16} />}
                            </div>


                            <div className={`flex flex-col gap-2 max-w-[80%] ${from === "user" ? "items-end" : ""}`}>
                                <div className={`p-4 rounded-2xl text-base leading-relaxed ${from === "user" ? "bg-primary text-primary-content shadow-lg shadow-primary/10" : "bg-base-200 text-base-content shadow-sm"}`}>
                                    {message.content}
                                </div>


                                {from === "assistant" && (
                                    <div className="flex items-center gap-2 px-1 text-[10px] font-bold uppercase tracking-tighter opacity-40">
                                        <Cpu size={12} />
                                        {message.adapter_version ? `Adapter v${message.adapter_version}` : "Base Model"}
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            <ChatComposer modelKey={modelKey} onSubmit={handleSend} isSubmitting={isRunningInference} />
        </div>
    );
};