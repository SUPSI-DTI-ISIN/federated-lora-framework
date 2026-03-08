import {Trash2} from "lucide-react";
import {useTranslation} from "react-i18next";
import {motion} from "framer-motion";
import {useState} from "react";
import {getModelKey} from "../../../utils/envUtils.ts";
import {useDeleteDepartmentAdapters} from "../../../hooks/department/mlflow/useDeleteDepartmentAdapters.ts";
import toast from "react-hot-toast";
import {DeleteConfirmModal} from "../../common/DeleteConfirmModal.tsx";

type DepartmentAdapterCardProps = {
    adapter: number;
};

export const DepartmentAdapterCard = ({adapter}: DepartmentAdapterCardProps) => {
    const {t} = useTranslation();
    const modelKey = getModelKey();

    const [isDeletingDepartmentAdapter, setIsDeletingDepartmentAdapter] = useState<boolean>(false);
    const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);
    const {mutateAsync: deleteDepartmentAdapter} = useDeleteDepartmentAdapters();

    const handleDelete = async () => {
        setShowDeleteModal(false);
        try {
            setIsDeletingDepartmentAdapter(true);
            await deleteDepartmentAdapter({modelKey, adapterVersion: adapter});
            toast.success(t("adapters.toast.deleted"));
        } catch (err: any) {
            console.error(err);
            toast.error(t("adapters.toast.error"));
        } finally {
            setIsDeletingDepartmentAdapter(false);
        }
    };

    return (
        <>
            <motion.div
                layout
                initial={{opacity: 0, y: 10}}
                animate={{opacity: 1, y: 0}}
                exit={{opacity: 0, scale: 0.98}}
                className="group w-full bg-base-100 p-4 sm:p-5 rounded-2xl border border-base-content/5 hover:border-info/30 hover:shadow-xl hover:shadow-info/5 transition-all duration-300"
            >
                <div className="flex flex-row items-center justify-between gap-6">

                    {/* Left Side: Version Indicator */}
                    <div className="flex items-center gap-5 min-w-0">
                        <div
                            className="flex flex-col items-center justify-center w-14 h-14 shrink-0 rounded-xl bg-base-200 text-base-content group-hover:bg-info group-hover:text-info-content transition-all duration-500 shadow-inner font-black">
                            <span className="text-[9px] uppercase opacity-50 mb-0.5 tracking-tighter">Ver</span>
                            <span className="text-xl leading-none">{adapter}</span>
                        </div>

                        <div className="truncate">
                            <h3 className="text-lg font-bold text-base-content truncate group-hover:text-info transition-colors">
                                {t("adapters.card.title", {version: adapter})}
                            </h3>
                        </div>
                    </div>

                    {/* Right Side: Action Button */}
                    <div className="flex items-center shrink-0">
                        <button
                            onClick={() => setShowDeleteModal(true)}
                            disabled={isDeletingDepartmentAdapter}
                            className="btn btn-ghost btn-circle text-error hover:bg-error/10"
                        >
                            {isDeletingDepartmentAdapter ? (
                                <span className="loading loading-spinner loading-sm"/>
                            ) : (
                                <Trash2 size={20} />
                            )}
                        </button>
                    </div>
                </div>
            </motion.div>

            <DeleteConfirmModal
                isOpen={showDeleteModal}
                onConfirm={handleDelete}
                onCancel={() => setShowDeleteModal(false)}
                itemName={t("adapters.card.title", {version: adapter})}
            />
        </>
    );
};