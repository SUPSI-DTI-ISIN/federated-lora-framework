import {MessageSquare, Trash2} from "lucide-react";
import {motion} from "framer-motion";
import type {ChatDTO} from "@isin/chat-service-client";

interface ChatListItemProps {
    chat: ChatDTO;
    isSelected: boolean;
    isDeleting: boolean;
    onSelect: () => void;
    onDelete: () => void;
    prefersReducedMotion: boolean;
}

export const ChatListItem = ({
                                 chat,
                                 isSelected,
                                 isDeleting,
                                 onSelect,
                                 onDelete,
                                 prefersReducedMotion,
                             }: ChatListItemProps) => {
    return (
        <motion.div
            variants={
                prefersReducedMotion
                    ? {}
                    : {
                        hidden: {opacity: 0, y: 8},
                        visible: {opacity: 1, y: 0},
                    }
            }
            className="flex items-center gap-2 w-full"
        >
            <button
                onClick={onSelect}
                className={`flex items-center gap-3 flex-1 p-3 rounded-xl transition-colors group justify-start ${
                    isSelected ? "bg-base-100 border border-primary" : "hover:bg-base-300"
                }`}
                aria-label={`Select chat: ${chat.title ?? `Chat #${chat.id}`}`}
                aria-current={isSelected ? "true" : undefined}
            >
                <MessageSquare size={18} className="shrink-0 opacity-50 group-hover:text-primary transition-colors"/>
                <div className="flex-1 flex items-center justify-between min-w-0">
          <span className="text-sm font-medium truncate opacity-80 group-hover:opacity-100">
            {chat.title ?? `Chat #${chat.id}`}
          </span>
                    <span className="text-xs opacity-40 ml-2 flex-shrink-0">
            {new Date(chat.created_at).toLocaleDateString()}
          </span>
                </div>
            </button>

            <button
                onClick={onDelete}
                className="btn btn-ghost btn-sm min-h-[44px] min-w-[44px] p-2"
                disabled={isDeleting}
                aria-label={`Delete chat: ${chat.title ?? `Chat #${chat.id}`}`}
            >
                {isDeleting ? <span className="loading loading-spinner loading-xs"></span> : <Trash2 size={16}/>}
            </button>
        </motion.div>
    );
}
