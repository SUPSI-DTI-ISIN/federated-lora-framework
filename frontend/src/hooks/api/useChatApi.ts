import {ChatApiContext} from "../../contexts/api/chatApiContext.ts";
import {useContext} from "react";

export const useChatApi = () => {
    const context = useContext(ChatApiContext);
    if (!context)
        throw new Error("useChatApi must be used within ChatApiProvider");
    return context;
};