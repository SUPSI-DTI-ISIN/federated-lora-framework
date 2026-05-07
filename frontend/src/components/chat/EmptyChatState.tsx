import {useTranslation} from "react-i18next";
import {Sparkles} from "lucide-react";

export const EmptyChatState = () => {
    const { t } = useTranslation();
    return (
        <div className="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-40">
            <Sparkles size={48} />
            <p className="max-w-xs text-lg font-medium">{t("chat.emptyHint") ?? "Seleziona o crea una chat per cominciare"}</p>
        </div>
    );
};