import { motion } from "framer-motion";
import { ChevronRight, Globe } from "lucide-react";
import type {InstituteDTO} from "@isin/institute-service-client";

interface RealmCardProps {
    realm: InstituteDTO;
    onSelect: (realm: InstituteDTO) => void;
}

export const RealmCard = ({ realm, onSelect }: RealmCardProps) => {
    return (
        <motion.div
            whileHover={{ y: -5, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="group cursor-pointer"
            onClick={() => onSelect(realm)}
        >
            <div className="card bg-base-100 border border-base-content/10 shadow-sm group-hover:shadow-xl group-hover:border-primary/30 transition-all duration-300">
                <div className="card-body p-6 flex-row items-center gap-5">
                    <div className="flex h-12 w-12 items-center justify-center bg-primary/10 rounded-xl text-primary group-hover:bg-primary group-hover:text-white transition-colors duration-300">
                        <Globe size={24} />
                    </div>

                    <div className="flex-1">
                        <h3 className="text-xl font-bold text-base-content group-hover:text-primary transition-colors">
                            {realm.name}
                        </h3>
                        <p className="text-sm text-base-content/50 font-medium">
                            url: {realm.url}
                        </p>
                    </div>

                    <ChevronRight className="text-base-content/20 group-hover:text-primary transition-colors" size={20} />
                </div>
            </div>
        </motion.div>
    );
};