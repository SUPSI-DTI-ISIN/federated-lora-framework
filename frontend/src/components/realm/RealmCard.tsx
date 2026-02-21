import { motion } from "framer-motion";
import {ChevronRight, Globe, Loader2, Trash2} from "lucide-react";
import type {InstituteDTO} from "@isin/institute-service-client";
import toast from "react-hot-toast";
import {useDeleteInstitute} from "../../hooks/department/institutes/useDeleteInstitute.ts";

interface RealmCardProps {
    realm: InstituteDTO;
    onSelect?: (realm: InstituteDTO) => void;
    isAdmin: boolean;
}

export const RealmCard = ({ realm, onSelect, isAdmin = false }: RealmCardProps) => {
    const { mutateAsync: deleteInstitute, isPending: isDeleting } = useDeleteInstitute();

    const handleDelete = async (e: React.MouseEvent) => {
        e.stopPropagation();
        if (window.confirm(`Eliminare definitivamente ${realm.name}?`)) {
            try {
                await deleteInstitute(realm.id!);
                toast.success("Istituto eliminato");
            } catch (err) {
                toast.error("Errore nell'eliminazione");
            }
        }
    };

    return (
        <motion.div
            whileHover={{ y: -5, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`group ${isAdmin? "" : "cursor-pointer"} relative`}
            onClick={() => onSelect? onSelect(realm) : () => {}}
        >
            <div className="card bg-base-100 border border-base-content/10 shadow-sm group-hover:shadow-xl group-hover:border-primary/30 transition-all duration-300">
                <div className="card-body p-6 flex-row items-center gap-5">
                    <div className="flex h-12 w-12 items-center justify-center bg-primary/10 rounded-xl text-primary group-hover:bg-primary group-hover:text-white transition-colors duration-300">
                        {isDeleting ? <Loader2 className="animate-spin" size={24}/> : <Globe size={24} />}
                    </div>

                    <div className="flex-1 truncate">
                        <h3 className="text-xl font-bold text-base-content group-hover:text-primary transition-colors truncate">
                            {realm.name}
                        </h3>
                        <p className="text-sm text-base-content/50 font-medium truncate">
                            {realm.url}
                        </p>
                    </div>

                    {isAdmin ? (
                        <button
                            onClick={handleDelete}
                            disabled={isDeleting}
                            className="btn btn-ghost btn-circle text-error/40 hover:text-error hover:bg-error/10 opacity-0 group-hover:opacity-100 transition-all"
                        >
                            <Trash2 size={20} />
                        </button>
                    ) : (
                        <ChevronRight className="text-base-content/20 group-hover:text-primary transition-colors" size={20} />
                    )}
                </div>
            </div>
        </motion.div>
    );
};