import {useState, useRef, useEffect} from "react";
import {User, LogOut} from "lucide-react";
import {motion, AnimatePresence} from "framer-motion";

interface ProfileDropdownProps {
    username: string;
    onLogout: () => void;
}

export const ProfileDropdown = ({username, onLogout}: ProfileDropdownProps) => {
    const [profileOpen, setProfileOpen] = useState(false);
    const profileRef = useRef<HTMLDivElement | null>(null);

    useEffect(() => {
        function handleClick(e: MouseEvent) {
            if (!profileRef.current) return;
            if (!profileRef.current.contains(e.target as Node)) {
                setProfileOpen(false);
            }
        }

        if (profileOpen) {
            document.addEventListener("mousedown", handleClick);
            return () => document.removeEventListener("mousedown", handleClick);
        }
    }, [profileOpen]);

    return (
        <div className="relative" ref={profileRef}>
            <button
                className="btn btn-ghost btn-circle"
                aria-label="Profile"
                onClick={() => setProfileOpen((s) => !s)}
                title={username}
            >
                <User size={18}/>
            </button>

            <AnimatePresence>
                {profileOpen && (
                    <motion.div
                        initial={{opacity: 0, scale: 0.95, y: -6}}
                        animate={{opacity: 1, scale: 1, y: 0}}
                        exit={{opacity: 0, scale: 0.95, y: -6}}
                        transition={{duration: 0.12}}
                        className="absolute right-0 mt-2 w-40 rounded-lg border bg-base-100 p-2 shadow-md"
                    >
                        <div className="flex flex-col gap-1">
                            <div className="px-2 py-1 text-xs text-base-content/70">
                                {username}
                            </div>
                            <button
                                className="flex w-full items-center gap-2 rounded-md px-2 py-2 text-sm hover:bg-base-200 cursor-pointer"
                                onClick={onLogout}
                            >
                                <LogOut size={16}/>
                                <span>Logout</span>
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}
