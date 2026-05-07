import { useState, useEffect } from "react";
import { Building, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import toast from "react-hot-toast";
import type { InstituteDTO } from "@isin/institute-service-client";
import { useUpdateInstitute } from "../../hooks/department/institutes/useUpdateInstitute.ts";

interface UpdateRealmModalProps {
    isOpen: boolean;
    onClose: () => void;
    institute: InstituteDTO | null;
}

export const UpdateRealmModal = ({ isOpen, onClose, institute }: UpdateRealmModalProps) => {

    const [name, setName] = useState("");
    const [url, setUrl] = useState("");

    const { mutateAsync: updateInstitute, isPending: isUpdating } = useUpdateInstitute();

    useEffect(() => {
        if (institute) {
            setName(institute.name ?? "");
            setUrl(institute.url ?? "");
        }
    }, [institute]);

    const handleUpdate = async () => {
        if (!institute?.id) return;

        try {
            await updateInstitute({
                instituteId: institute.id,
                updateInstituteBody: {
                    name,
                    url
                }
            });

            toast.success("Istituto aggiornato con successo!");
            onClose();
        } catch (e) {
            toast.error("Errore durante l'aggiornamento");
        }
    };

    if (!isOpen || !institute) return null;

    return (
        <div className="modal modal-open backdrop-blur-sm bg-base-content/20">
            <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="modal-box border border-base-content/10 p-0"
            >
                <div className="p-6 border-b border-base-content/5 flex justify-between items-center bg-base-200/50">
                    <h3 className="text-xl font-bold flex items-center gap-2">
                        <Building className="text-primary" size={22}/>
                        Modifica Istituto
                    </h3>
                </div>

                <div className="p-6 space-y-4">
                    <div className="form-control">
                        <label className="label mr-2 text-xs font-bold uppercase text-base-content/50">
                            Nome Istituto
                        </label>

                        <input
                            className="input input-bordered focus:input-primary transition-all bg-base-100"
                            placeholder="Es: Dipartimento di Informatica"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                    </div>

                    <div className="form-control">
                        <div className="join w-full">
                            <label className="label mr-2 text-xs font-bold uppercase text-base-content/50">
                                URL Endpoint
                            </label>

                            <input
                                className="input input-bordered join-item flex-1 focus:input-primary transition-all bg-base-100"
                                placeholder="https://api.institute.it"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                            />
                        </div>
                    </div>
                </div>

                <div className="p-6 bg-base-200/30 flex gap-3">
                    <button
                        className="btn btn-ghost flex-1"
                        onClick={onClose}
                        disabled={isUpdating}
                    >
                        Annulla
                    </button>

                    <button
                        className="btn btn-primary flex-1 shadow-lg shadow-primary/20"
                        onClick={handleUpdate}
                        disabled={isUpdating || !name || !url}
                    >
                        {isUpdating ? <Loader2 className="animate-spin"/> : "Aggiorna Istituto"}
                    </button>
                </div>
            </motion.div>
        </div>
    );
};