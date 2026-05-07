import {useEffect, useState} from "react";
import {
    ChevronDown,
    ChevronUp,
    FileCog,
} from "lucide-react";
import {AnimatePresence, motion} from "framer-motion";
import {useTranslation} from "react-i18next";
import type {DocumentDTO} from "@isin/data-service-client";
import {
    useUpdateDocumentExternalApproved
} from "../../hooks/institute/data/documents/useUpdateDocumentExternalApproved.ts";
import {useUpdateDocumentTrainability} from "../../hooks/institute/data/documents/useUpdateDocumentTrainability.ts";
import toast from "react-hot-toast";

interface DocumentSettingsCardProps {
    document: DocumentDTO
}

export const DocumentSettingsCard = ({document}: DocumentSettingsCardProps) => {
    const {t} = useTranslation();

    const [isOpen, setIsOpen] = useState(false);
    const {mutateAsync: updateDocumentTrainability} = useUpdateDocumentTrainability();
    const {mutateAsync: updateDocumentExternalApproved} = useUpdateDocumentExternalApproved();

    const [isUpdatingTrainable, setIsUpdatingTrainable] = useState(false);
    const [isUpdatingExternalApproved, setIsUpdatingExternalApproved] = useState(false);

    const [localTrainable, setLocalTrainable] = useState(document.is_trainable);
    const [localExternalApproved, setLocalExternalApproved] = useState(document.is_externally_approved);

    useEffect(() => {
        setLocalTrainable(document.is_trainable);
        setLocalExternalApproved(document.is_externally_approved);
    }, [document.is_trainable, document.is_externally_approved]);

    const handleTrainableChange = async (checked: boolean) => {
        setLocalTrainable(checked);
        try {
            setIsUpdatingTrainable(true);
            await updateDocumentTrainability({
                documentId: document.id,
                isTrainable: checked,
            });
            toast.success(t("sections.settings.trainable.success"));
        } catch (e) {
            console.error(e);
            setLocalTrainable(!checked);
            toast.error(t("sections.settings.trainable.error"));
        } finally {
            setIsUpdatingTrainable(false);
        }
    };

    const handleExternalApprovedChange = async (checked: boolean) => {
        setLocalExternalApproved(checked);
        try {
            setIsUpdatingExternalApproved(true);
            await updateDocumentExternalApproved({
                documentId: document.id,
                isExternallyApproved: checked,
            });
            toast.success(t("sections.settings.externalApproved.success"));
        } catch (e) {
            console.error(e);
            setLocalExternalApproved(!checked);
            toast.error(t("sections.settings.externalApproved.error"));
        } finally {
            setIsUpdatingExternalApproved(false);
        }
    };

    return (
        <div className="bg-base-100 rounded-2xl border border-base-content/5 shadow-sm overflow-hidden mb-6">
            <button
                onClick={() => setIsOpen((prev) => !prev)}
                className="w-full flex items-center justify-between px-6 py-4 hover:bg-base-200/50 transition-colors cursor-pointer"
            >
                <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary/10 text-primary">
                        <FileCog size={20}/>
                    </div>

                    <div className="flex flex-col items-start">
                        <span className="font-bold text-base-content">
                            {t("sections.settings.title")}
                        </span>
                        <span className="text-xs text-base-content/50">
                            {t("sections.settings.subtitle")}
                        </span>
                    </div>
                </div>

                {isOpen ? (
                    <ChevronUp size={18} className="text-base-content/40"/>
                ) : (
                    <ChevronDown size={18} className="text-base-content/40"/>
                )}
            </button>

            <AnimatePresence initial={false}>
                {isOpen && (
                    <motion.div
                        initial={{height: 0, opacity: 0}}
                        animate={{height: "auto", opacity: 1}}
                        exit={{height: 0, opacity: 0}}
                        transition={{duration: 0.2}}
                        className="overflow-hidden"
                    >
                        <div className="px-6 pb-6 pt-2 space-y-6">

                            {/* Trainable */}
                            <div className="flex items-center justify-between gap-4">
                                <div>
                                    <h3 className="font-semibold">
                                        {t("sections.settings.trainable.title")}
                                    </h3>
                                    <p className="text-sm text-base-content/60 mt-1">
                                        {t("sections.settings.trainable.description")}
                                    </p>
                                </div>

                                {isUpdatingTrainable ? (
                                    <span className="loading loading-spinner loading-sm text-primary"/>
                                ) : (
                                    <input
                                        type="checkbox"
                                        className="toggle toggle-primary"
                                        checked={localTrainable}
                                        onChange={(e) => handleTrainableChange(e.target.checked)}
                                    />
                                )}
                            </div>

                            {/* External Approved */}
                            <div className="flex items-center justify-between gap-4">
                                <div>
                                    <h3 className="font-semibold">
                                        {t("sections.settings.externalApproved.title")}
                                    </h3>
                                    <p className="text-sm text-base-content/60 mt-1">
                                        {t("sections.settings.externalApproved.description")}
                                    </p>
                                </div>

                                {isUpdatingExternalApproved ? (
                                    <span className="loading loading-spinner loading-sm text-primary"/>
                                ) : (
                                    <input
                                        type="checkbox"
                                        className="toggle toggle-primary"
                                        checked={localExternalApproved}
                                        onChange={(e) => handleExternalApprovedChange(e.target.checked)}
                                    />
                                )}
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};