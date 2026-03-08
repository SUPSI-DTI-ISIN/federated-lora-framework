import { useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {Send} from "lucide-react";
import {useGetAllAvailableLocalAdapters} from "../../hooks/institute/model/useGetAllAvailableLocalAdapters.ts";

type ChatComposerProps = {
    modelKey: string;
    onSubmit: (prompt: string, adapterVersion?: number | null ) => Promise<void>;
    isSubmitting?: boolean;
};

export const ChatComposer = ({ modelKey, onSubmit, isSubmitting = false }: ChatComposerProps) => {
    const { t } = useTranslation();
    const { data: availableAdaptersDTO } = useGetAllAvailableLocalAdapters(modelKey);
    const adapters = availableAdaptersDTO?.adapters ?? [];

    const [prompt, setPrompt] = useState("");
    const [selectedAdapterVersion, setSelectedAdapterVersion] = useState<number | null>(null);
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setPrompt(e.target.value);
        const target = e.target;
        target.style.height = "auto";
        target.style.height = `${Math.min(target.scrollHeight, 200)}px`;
    };

    const handleSubmit = async () => {
        if (!prompt.trim() || isSubmitting) return;
        await onSubmit(prompt.trim(), selectedAdapterVersion);
        setPrompt("");
        if (textareaRef.current) textareaRef.current.style.height = "auto";
    };

    return (
        <div className="p-4 sm:p-6 bg-linear-to-t from-base-100 via-base-100 to-transparent w-full">
            <div className="max-w-5xl mx-auto relative bg-base-200 rounded-3xl p-2 border border-base-content/10 shadow-2xl focus-within:border-primary/30 transition-all">

                <div className="flex items-center gap-2 px-2 pb-2 mb-2 border-b border-base-content/5">
                    <span className="text-[10px] font-black uppercase opacity-40 ml-1">{t("chat.adapter.chooseLabel")}</span>
                    <select
                        className="select select-ghost select-xs font-bold text-primary focus:bg-transparent"
                        value={selectedAdapterVersion ?? ""}
                        onChange={(e) => setSelectedAdapterVersion(e.target.value ? Number(e.target.value) : null)}
                    >
                        <option value="">{t("chat.adapter.baseModelLabel")}</option>
                        {adapters.map((a: any) => (
                            <option key={a.version} value={a.version}>v{a.version}</option>
                        ))}
                    </select>
                </div>

                <div className="flex items-end gap-2">
                    <textarea
                        ref={textareaRef}
                        rows={1}
                        value={prompt}
                        onChange={handleInput}
                        onKeyDown={(e) => {
                            if (e.key === "Enter" && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit();
                            }
                        }}
                        placeholder={t("chat.startPromptPlaceholder") ?? "Scrivi un messaggio..."}
                        className="textarea textarea-ghost w-full resize-none bg-transparent focus:outline-none py-3 px-4 text-base min-h-13"
                    />

                    <button
                        onClick={handleSubmit}
                        disabled={isSubmitting || !prompt.trim()}
                        className={`btn btn-circle btn-primary mb-1 mr-1 transition-all ${isSubmitting ? "loading" : ""}`}
                    >
                        {!isSubmitting && <Send size={18} />}
                    </button>
                </div>
            </div>
            <p className="text-[10px] text-center mt-3 opacity-30 font-medium">{t("chat.disclaimer")}</p>
        </div>
    );
};