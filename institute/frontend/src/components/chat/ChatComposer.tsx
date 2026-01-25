import { useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { ChevronDown } from "lucide-react";
import {useGetAllAvailableLocalAdapters} from "../../hooks/model/useGetAllAvailableLocalAdapters.ts";
import type {InferenceModelParams} from "../../hooks/inference/useInferenceModel.ts";

type ChatComposerProps = {
    modelKey: string;
    onSubmit: (inferenceParams: InferenceModelParams) => Promise<void>;
    isSubmitting?: boolean;
};

export const ChatComposer = ({ modelKey, onSubmit, isSubmitting = false }: ChatComposerProps) => {
    const { t } = useTranslation();
    const { data: availableAdaptersDTO, isLoading: loadingAdapters } = useGetAllAvailableLocalAdapters(modelKey);
    const adapters = availableAdaptersDTO?.adapters ?? [];

    const [prompt, setPrompt] = useState<string>("");
    const [selectedAdapterVersion, setSelectedAdapterVersion] = useState<number | null>(null);
    const inputRef = useRef<HTMLInputElement | null>(null);


    const handleSubmit = async () => {
        if (!prompt.trim()) return;
        await onSubmit({
            modelKey: modelKey,
            prompt: prompt.trim(),
            adapterVersion: selectedAdapterVersion
        });
        setPrompt("");
    };

    return (
        <div className="border-t border-base-300 p-4 bg-base-100">
            <div className="flex gap-3 items-center">
                {/* Adapter select */}
                <div className="flex items-center gap-2">
                    <label className="sr-only">{t("chat.adapter.selectLabel")}</label>
                    <div className="relative">
                        <select
                            className="select select-bordered select-sm"
                            aria-label={t("chat.adapter.selectLabel") as string}
                            value={selectedAdapterVersion ?? ""}
                            onChange={(e) => {
                                const v = e.target.value;
                                setSelectedAdapterVersion(v === "" ? null : Number(v));
                            }}
                            disabled={loadingAdapters}
                        >
                            <option value="">{t("chat.adapter.baseModelLabel")}</option>
                            {adapters.map((a) => (
                                <option key={String(a.version)} value={String(a.version)}>
                                    {`v${a.version} ${a.available_local ? `(${t("chat.adapter.local")})` : ""}`}
                                </option>
                            ))}
                        </select>
                        <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" size={14} />
                    </div>
                </div>

                {/* Input */}
                <input
                    ref={inputRef}
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={async (e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                            e.preventDefault();
                            await handleSubmit();
                        }
                    }}
                    placeholder={t("chat.startPromptPlaceholder")}
                    className="input input-bordered flex-1"
                    aria-label={t("chat.startPromptPlaceholder") as string}
                />

                {/* Send */}
                <div className="flex items-center gap-2">
                    <button
                        className="btn btn-ghost"
                        onClick={() => {
                            setPrompt("");
                        }}
                        disabled={isSubmitting}
                        title={t("common.clear") as string}
                    >
                        {t("common.clear")}
                    </button>

                    <button
                        className="btn btn-primary"
                        onClick={handleSubmit}
                        disabled={isSubmitting || !prompt.trim()}
                        aria-label={t("chat.sendButton") as string}
                    >
                        {isSubmitting ? t("chat.sending") : t("chat.sendButton")}
                    </button>
                </div>
            </div>
        </div>
    );
};
