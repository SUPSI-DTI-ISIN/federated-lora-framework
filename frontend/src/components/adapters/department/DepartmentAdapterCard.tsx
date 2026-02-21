import {Trash2} from "lucide-react";
import {useTranslation} from "react-i18next";
import {motion} from "framer-motion";
import {useState} from "react";
import {getModelKey} from "../../../utils/envUtils.ts";
import {useDeleteDepartmentAdapters} from "../../../hooks/department/mlflow/useDeleteDepartmentAdapters.ts";
import toast from "react-hot-toast";

type DepartmentAdapterCardProps = {
    adapter: number;
};

export const DepartmentAdapterCard = ({adapter}: DepartmentAdapterCardProps) => {
    const {t} = useTranslation();
    const modelKey = getModelKey();

    const [isDeletingDepartmentAdapter, setIsDeletingDepartmentAdapter] = useState<boolean>(false);
    const {mutateAsync: deleteDepartmentAdapter} = useDeleteDepartmentAdapters();

    const handleDelete = async () => {
        try {
            setIsDeletingDepartmentAdapter(true);
            await deleteDepartmentAdapter({modelKey, adapterVersion: adapter});
            toast.success("Delete department adapter successfully");
        } catch (err: any) {
            console.error(err);
            toast.error("Error deleting department adapter");
        } finally {
            setIsDeletingDepartmentAdapter(false);
        }
    };

    return (
        <motion.div
            layout
            initial={{opacity: 0, y: 10}}
            animate={{opacity: 1, y: 0}}
            exit={{opacity: 0, scale: 0.98}}
            className="group w-full bg-base-100 p-4 sm:p-5 rounded-2xl border border-base-content/5 hover:border-secondary/30 hover:shadow-xl hover:shadow-secondary/5 transition-all duration-300"
        >
            <div className="flex flex-row items-center justify-between gap-6">

                {/* Left Side: Version Indicator */}
                <div className="flex items-center gap-5 min-w-0">
                    <div
                        className="flex flex-col items-center justify-center w-14 h-14 shrink-0 rounded-xl bg-base-200 text-base-content group-hover:bg-secondary group-hover:text-secondary-content transition-all duration-500 shadow-inner font-black">
                        <span className="text-[9px] uppercase opacity-50 mb-0.5 tracking-tighter">Ver</span>
                        <span className="text-xl leading-none">{adapter}</span>
                    </div>

                    <div className="truncate">
                        <h3 className="text-lg font-bold text-base-content truncate group-hover:text-secondary transition-colors">
                            {t("adapters.card.title", {adapter})}
                        </h3>
                    </div>
                </div>

                {/* Right Side: Action Button */}
                <div className="flex items-center shrink-0">
                    <button
                        onClick={handleDelete}
                        disabled={isDeletingDepartmentAdapter}
                        className={`
                                btn btn-md sm:btn-lg rounded-2xl
                                ${isDeletingDepartmentAdapter ? 'btn-ghost' : 'btn-secondary'} 
                                shadow-lg shadow-secondary/20 hover:scale-105 transition-all
                                px-6
                            `}
                    >
                        {isDeletingDepartmentAdapter ? (
                            <span className="loading loading-spinner"/>
                        ) : (
                            <>
                                <Trash2 size={20} className="mr-2"/>
                                <span className="hidden sm:inline">{t("adapters.delete")}</span>
                            </>
                        )}
                    </button>
                </div>
            </div>
        </motion.div>
    );
};