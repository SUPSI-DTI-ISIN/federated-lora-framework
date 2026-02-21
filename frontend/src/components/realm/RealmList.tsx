import type {InstituteDTO} from "@isin/institute-service-client";
import { motion } from "framer-motion";
import {RealmCard} from "./RealmCard.tsx";

interface RealmListProps {
    realms: InstituteDTO[];
    onSelectRealm?: (realm: InstituteDTO) => void;
    isAdmin?: boolean;
}

export const RealmList = ({realms, onSelectRealm, isAdmin = false}: RealmListProps) => {

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
            {realms.map((institute, index) => (
                <motion.div
                    key={institute.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.05 }}
                >
                    <RealmCard
                        realm={institute}
                        onSelect={onSelectRealm}
                        isAdmin={isAdmin}
                    />
                </motion.div>
            ))}
        </motion.div>
    )
}