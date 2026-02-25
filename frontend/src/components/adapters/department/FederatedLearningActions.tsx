import { useState } from "react";
import { Play, ExternalLink, Loader2 } from "lucide-react";
import { toast } from "react-hot-toast";
import {useStartFederatedLearning} from "../../../hooks/department/federated-learning/useStartFederatedLearning.ts";
import {getFlowerCeleryJobsUrl} from "../../../utils/envUtils.ts";


export const FederatedLearningActions = () => {
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
        <div className="flex items-center gap-2 pl-4 ml-4 border-l border-base-content/10">
            <button
                onClick={handleStartFL}
                disabled={isStarting}
                className="btn btn-primary btn-sm normal-case gap-2"
            >
                {isStarting ? (
                    <Loader2 size={16} className="animate-spin" />
                ) : (
                    <Play size={16} fill="currentColor" />
                )}
                <span>Start Federated Learning</span>
            </button>

            <a
                href={getFlowerCeleryJobsUrl()}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-ghost btn-sm btn-square"
                title="Track background jobs"
            >
                <ExternalLink size={18} className="text-base-content/60 hover:text-secondary transition-colors" />
            </a>
        </div>
    );
};