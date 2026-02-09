import {EmptyChatState} from "./EmptyChatState.tsx";
import {ChatInterface} from "./ChatInterface.tsx";

interface ChatInterfaceWrapperProps {
    modelKey: string;
    chatId: number | null;
}

export const ChatInterfaceWrapper = ({ modelKey, chatId }: ChatInterfaceWrapperProps) => {
    if (chatId === null) {
        return <EmptyChatState />;
    }


    return <ChatInterface modelKey={modelKey} chatId={chatId} />;
};