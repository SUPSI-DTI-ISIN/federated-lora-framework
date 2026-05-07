import { useState } from "react";
import { Building, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import {useCreateInstitute} from "../../hooks/department/institutes/useCreateInstitute.ts";
import toast from "react-hot-toast";
import type {InstituteCreationRequestDTO} from "@isin/institute-service-client";

export const CreateRealmModal = ({ isOpen, onClose }: any) => {
    const [form, setForm] = useState<InstituteCreationRequestDTO>({ name: "", url: "" });

    const { mutateAsync: createInstitute, isPending: isCreating } = useCreateInstitute();

    const handleCreate = async () => {
        try {
            await createInstitute(form);
            toast.success("Istituto creato con successo!");
            setForm({name: "", url: ""});
            onClose();
        } catch (e) {
            toast.error("Errore durante la creazione");
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal modal-open backdrop-blur-sm bg-base-content/20">
            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="modal-box border border-base-content/10 p-0">
                <div className="p-6 border-b border-base-content/5 flex justify-between items-center bg-base-200/50">
                    <h3 className="text-xl font-bold flex items-center gap-2"><Building className="text-primary" size={22}/> Nuovo Istituto</h3>
                </div>

                <div className="p-6 space-y-4">
                    <div className="form-control">
                        <label className="label mr-2 text-xs font-bold uppercase text-base-content/50">Nome Istituto</label>
                        <input
                            className="input input-bordered focus:input-primary transition-all bg-base-100"
                            placeholder="Es: Dipartimento di Informatica"
                            value={form.name}
                            onChange={e => setForm({...form, name: e.target.value})}
                        />
                    </div>

                    <div className="form-control">
                        <div className="join w-full">
                            <label className="label mr-2 text-xs font-bold uppercase text-base-content/50">URL Endpoint</label>
                            <input
                                className="input input-bordered join-item flex-1 focus:input-primary transition-all bg-base-100"
                                placeholder="https://api.institute.it"
                                value={form.url}
                                onChange={e => {
                                    setForm({...form, url: e.target.value});
                                }}
                            />

                        </div>
                    </div>
                </div>

                <div className="p-6 bg-base-200/30 flex gap-3">
                    <button className="btn btn-ghost flex-1" onClick={onClose} disabled={isCreating}>Annulla</button>
                    <button className="btn btn-primary flex-1 shadow-lg shadow-primary/20"
                            onClick={handleCreate} disabled={isCreating || !form.name || !form.url}>
                        {isCreating ? <Loader2 className="animate-spin" /> : "Salva Istituto"}
                    </button>
                </div>
            </motion.div>
        </div>
    );
};