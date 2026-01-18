import { AnimatePresence } from 'framer-motion';
import { ChevronLeft, ChevronRight} from 'lucide-react';

interface ChatSidebarProps {
    isOpen: boolean;
    onToggle: () => void;
}

export const ChatSidebar = ({ isOpen, onToggle }: ChatSidebarProps) => {
    return (
        <>
            {/* Toggle Button */}
            <button
                onClick={onToggle}
                className="fixed left-4 top-24 z-30 btn btn-circle btn-sm bg-base-200 shadow-lg lg:hidden"
            >
                {isOpen ? <ChevronLeft size={18} /> : <ChevronRight size={18} />}
            </button>

            {/* Sidebar */}
            <AnimatePresence>
                {isOpen && (
                    <>
                    </>
                )}
            </AnimatePresence>
        </>
    );
};