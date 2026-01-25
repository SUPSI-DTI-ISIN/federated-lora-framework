import {useEffect, useRef, useState} from "react";
import {useTranslation} from "react-i18next";
import toast from "react-hot-toast";
import {ChatComposer} from "./ChatComposer";
import {type InferenceModelParams, useInferenceModel} from "../../hooks/inference/useInferenceModel.ts";

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
        <div className="h-full flex flex-col">
            {/* Messages */}
            <div className="flex-1 overflow-auto p-6 space-y-4" ref={scrollRef} role="log" aria-live="polite">
                {messages.length === 0 && (
                    <div className="text-center text-base-content/60">{t("chat.emptyHint")}</div>
                )}

                {messages.map((message) => (
                    <div key={message.id} className={`max-w-3xl ${message.from === "user" ? "ml-auto text-right" : ""}`}>
                        <div
                            className={`inline-block p-3 rounded-lg wrap-break-word ${
                                message.from === "user" ? "bg-primary text-primary-content" : "bg-base-200"
                            }`}
                        >
                            {message.text}
                            {message.from === "assistant" && message.modelKey && (
                                <div className="text-xs text-base-content/50 mt-1">
                                    {message.adapterVersion !== null
                                        ? `${message.modelKey} (v${message.adapterVersion})`
                                        : `${message.modelKey} (base)`}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Composer */}
            <ChatComposer
                modelKey={modelKey}
                onSubmit={handleSend}
                isSubmitting={isRunningInference}
            />
        </div>
    );
};