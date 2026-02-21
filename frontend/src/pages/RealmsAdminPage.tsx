import {useTranslation} from "react-i18next";
import {motion, AnimatePresence} from "framer-motion";
import {LayoutGrid, AlertCircle, Plus} from "lucide-react";
import {useGetAllInstitutes} from "../hooks/department/institutes/useGetAllInstitutes.ts";
import {RealmList} from "../components/realm/RealmList.tsx";
import {useAuthWrapper} from "../hooks/auth/useAuthWrapper.ts";
import {useNavigate} from "react-router-dom";
import {useEffect, useState, useMemo} from "react";
import {RealmSearchBar} from "../components/realm/RealmSearchBar.tsx";
import {CreateRealmModal} from "../components/realm/CreateRealmModal.tsx";

export const RealmsAdminPage = () => {
    const {t} = useTranslation();
    const [searchQuery, setSearchQuery] = useState("");
    const [isModalOpen, setIsModalOpen] = useState(false);

    const {data: realms, isLoading, error} = useGetAllInstitutes();
    const {isDepartmentAdmin} = useAuthWrapper();
    const navigate = useNavigate();

    useEffect(() => {
        if (!isDepartmentAdmin) navigate("/");
    }, [isDepartmentAdmin, navigate]);

    const filteredRealms = useMemo(() => {
        if (!realms) return [];
        return realms.filter((r) =>
            r.name.toLowerCase().includes(searchQuery.toLowerCase())
        );
    }, [realms, searchQuery]);

    if (isLoading) {
        return (
            <div className="min-h-screen bg-base-100 py-12 px-6">
                <div className="max-w-7xl mx-auto space-y-8">
                    <div className="h-20 bg-base-200 rounded-3xl animate-pulse w-1/2"/>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[1, 2, 3, 4, 5, 6].map((i) => (
                            <div key={i} className="h-24 bg-base-200 rounded-2xl animate-pulse"/>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    if (error || !realms) {
        return (
            <div className="min-h-screen flex items-center justify-center p-6">
                <div className="max-w-md w-full card bg-error/10 border border-error/20 p-8 text-center">
                    <AlertCircle className="mx-auto text-error mb-4" size={48} />
                    <h3 className="text-xl font-bold text-error mb-2">Errore di caricamento</h3>
                    <p className="text-error/70">Impossibile recuperare la lista dei realms. Riprova più tardi.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-base-100 py-12 px-4 sm:px-8 relative overflow-hidden">
            <div
                className="absolute top-0 left-1/4 -translate-y-1/2 w-96 h-96 bg-primary/5 blur-[120px] rounded-full -z-10"/>

            <div className="relative z-10 max-w-7xl mx-auto">
                <motion.div
                    initial={{opacity: 0, y: -10}}
                    animate={{opacity: 1, y: 0}}
                    className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8"
                >
                    <div className="flex items-center gap-5">
                        <div
                            className="flex h-16 w-16 items-center justify-center bg-primary/10 rounded-2xl text-primary shadow-inner">
                            <LayoutGrid size={36}/>
                        </div>
                        <div>
                            <h1 className="text-4xl font-black tracking-tight text-base-content leading-none mb-2">
                                {t("realms.title", "Istituti")}
                            </h1>
                            <p className="text-lg text-base-content/60 font-medium">
                                Gestione amministrativa dei realm
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="btn btn-primary btn-lg rounded-2xl shadow-xl shadow-primary/20 hover:scale-105 transition-all gap-2"
                    >
                        <Plus size={24}/>
                        Nuovo Istituto
                    </button>
                </motion.div>

                <RealmSearchBar value={searchQuery} onChange={setSearchQuery}/>

                <div className="mt-4">
                    <RealmList realms={filteredRealms} isAdmin={isDepartmentAdmin}/>
                </div>

                {filteredRealms.length === 0 && searchQuery && (
                    <div className="text-center py-20 opacity-40">
                        <p className="text-xl font-medium">Nessun istituto corrisponde alla ricerca.</p>
                    </div>
                )}
            </div>

            <AnimatePresence>
                {isModalOpen && (
                    <CreateRealmModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}/>
                )}
            </AnimatePresence>
        </div>
    );
};