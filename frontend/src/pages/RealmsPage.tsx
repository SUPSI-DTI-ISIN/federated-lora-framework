import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import { LayoutGrid, AlertCircle } from "lucide-react";
import { useSelectorRealm } from "../hooks/realm/useSelectorRealm.ts";
import { useGetAllInstitutes } from "../hooks/institutes/useGetAllInstitutes.ts";
import type {InstituteDTO} from "@isin/institute-service-client";
import {RealmList} from "../components/realm/RealmList.tsx";

export const RealmsPage = () => {
    const { t } = useTranslation();
    const { setRealm } = useSelectorRealm();
    const { data: realms, isLoading, error } = useGetAllInstitutes();

    const handleSelectRealm = (realm: InstituteDTO) => {
        setRealm(realm.name);
    }

    if (isLoading) {
        return (
            <div className="min-h-screen bg-base-100 py-12 px-6">
                <div className="max-w-7xl mx-auto space-y-8">
                    <div className="h-20 bg-base-200 rounded-3xl animate-pulse w-1/2" />
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {[1, 2, 3, 4, 5, 6].map((i) => (
                            <div key={i} className="h-24 bg-base-200 rounded-2xl animate-pulse" />
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
            {/* Background Decoration */}
            <div className="absolute top-0 left-1/4 -translate-y-1/2 w-96 h-96 bg-primary/5 blur-[120px] rounded-full -z-10" />

            <div className="relative z-10 max-w-7xl mx-auto">
                {/* Header della Pagina */}
                <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12"
                >
                    <div className="flex items-center gap-5">
                        <div className="flex h-16 w-16 items-center justify-center bg-primary/10 rounded-2xl text-primary shadow-inner">
                            <LayoutGrid size={36} />
                        </div>
                        <div>
                            <h1 className="text-4xl font-black tracking-tight text-base-content leading-none mb-2">
                                {t("realms.title", "Istituti")}
                            </h1>
                            <p className="text-lg text-base-content/60 font-medium">
                                {t("realms.subtitle", "Seleziona un ambito di lavoro per iniziare")}
                            </p>
                        </div>
                    </div>
                </motion.div>

                {/* Grid dei Realms */}
                <RealmList realms={realms} onSelectRealm={handleSelectRealm} />
            </div>
        </div>
    );
};