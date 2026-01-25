import {useEffect, useRef, useState} from "react";
import {useTranslation} from "react-i18next";
import toast from "react-hot-toast";
import {ChatComposer} from "./ChatComposer";
import {type InferenceModelParams, useInferenceModel} from "../../hooks/inference/useInferenceModel.ts";
import {Cpu, Sparkles, User} from "lucide-react";

type Message = {
    id: string;
    from: "user" | "assistant" | "system";
    text: string;
    modelKey?: string;
    adapterVersion?: number | null;
};

interface ChatInterfaceProps {
    modelKey: string;
}

export const ChatInterface = ({
                                  modelKey,
                              }: ChatInterfaceProps) => {

    const {t} = useTranslation();
    const [messages, setMessages] = useState<Message[]>([]);
    const scrollRef = useRef<HTMLDivElement | null>(null);

    const [isRunningInference, setIsRunningInference] = useState<boolean>(false);
    const {mutateAsync: runInference} = useInferenceModel();

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const appendMessage = (m: Message) => setMessages((prev) => [...prev, m]);

    const handleSend = async (inferenceParams: InferenceModelParams) => {
        const userId = String(Date.now());
        appendMessage({id: userId, from: "user", text: inferenceParams.prompt});

        setIsRunningInference(true);
        try {
            const res = await runInference({
                modelKey: inferenceParams.modelKey,
                adapterVersion: inferenceParams.adapterVersion,
                prompt: inferenceParams.prompt
            });

            appendMessage({
                id: userId + "-r",
                from: "assistant",
                text: res.response,
                modelKey: res.model_key,
                adapterVersion: res.adapter_version,
            });
        } catch (err: any) {
            console.error(err);
            toast.error(t("chat.errorInference"));
            appendMessage({
                id: userId + "-r",
                from: "assistant",
                text: t("chat.errorInference"),
            });
        } finally {
            setIsRunningInference(false);
        }
    };

    return (
        <div className="h-full flex flex-col max-w-4xl mx-auto w-full">
            <div className="flex-1 overflow-y-auto p-4 sm:p-8 space-y-8 scroll-smooth" ref={scrollRef}>
                {messages.length === 0 && (
                    <div className="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-40">
                        <Sparkles size={48}/>
                        <p className="max-w-xs text-lg font-medium">{t("chat.emptyHint")}</p>
                    </div>
                )}

                {messages.map((message) => (
                    <div key={message.id} className={`flex gap-4 ${message.from === "user" ? "flex-row-reverse" : ""}`}>
                        <div className={`h-8 w-8 rounded-full flex items-center justify-center shrink-0 ${
                            message.from === "user" ? "bg-primary text-primary-content" : "bg-secondary text-secondary-content"
                        }`}>
                            {message.from === "user" ? <User size={16}/> : <Sparkles size={16}/>}
                        </div>

                        <div
                            className={`flex flex-col gap-2 max-w-[80%] ${message.from === "user" ? "items-end" : ""}`}>
                            <div className={`p-4 rounded-2xl text-base leading-relaxed ${
                                message.from === "user"
                                    ? "bg-primary text-primary-content shadow-lg shadow-primary/10"
                                    : "bg-base-200 text-base-content shadow-sm"
                            }`}>
                                {message.text}
                            </div>

                            {message.from === "assistant" && (
                                <div
                                    className="flex items-center gap-2 px-1 text-[10px] font-bold uppercase tracking-tighter opacity-40">
                                    <Cpu size={12}/>
                                    {message.adapterVersion ? `Adapter v${message.adapterVersion}` : "Base Model"}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            <ChatComposer modelKey={modelKey} onSubmit={handleSend} isSubmitting={isRunningInference}/>
        </div>
    );
};