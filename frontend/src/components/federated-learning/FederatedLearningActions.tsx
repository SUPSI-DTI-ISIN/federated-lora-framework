import { useState } from "react";
import { Play, ExternalLink, Loader2 } from "lucide-react";
import { toast } from "react-hot-toast";
import {useStartFederatedLearning} from "../../hooks/department/federated-learning/useStartFederatedLearning.ts";
import {getFlowerCeleryJobsUrl} from "../../utils/envUtils.ts";
import {useTranslation} from "react-i18next";


export const FederatedLearningActions = () => {
    const {t} = useTranslation();
    const { mutateAsync: startFederatedLearning } = useStartFederatedLearning();
    const [isStarting, setIsStarting] = useState<boolean>(false);

    const handleStartFL = async () => {
        try {
            setIsStarting(true);
            await startFederatedLearning();
            toast.success("Federated learning fine tuning started successfully");
        } catch (err: any) {
            console.error(err);
            toast.error("Error starting federated learning");
        } finally {
            setIsStarting(false);
        }
    };

    return (
        <div className="flex items-center gap-3 shrink-0">
            <button
                onClick={handleStartFL}
                disabled={isStarting}
                className="btn btn-primary gap-2"
            >
                {isStarting ? (
                    <Loader2 size={18} className="animate-spin" />
                ) : (
                    <Play size={18} fill="currentColor" />
                )}
                <span>{t("adapters.admin.fl.start")}</span>
            </button>

            <a
                href={getFlowerCeleryJobsUrl()}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-ghost btn-square"
                title={t("adapters.admin.fl.trackJobs")}
            >
                <ExternalLink size={20} />
            </a>
        </div>
    );
};