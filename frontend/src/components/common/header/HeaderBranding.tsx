import {Link} from "react-router-dom";
import {useTranslation} from "react-i18next";
import {motion} from "framer-motion";
import petallogo from "../../../assets/petal-logo.png";

interface HeaderBrandingProps {
    isAuthenticated: boolean;
    realm?: string;
}

export const HeaderBranding = (({isAuthenticated, realm}: HeaderBrandingProps) => {
    const {t} = useTranslation();

    return (
        <Link
            to="/"
            className="group flex items-center gap-3 focus-visible:outline-primary rounded-lg transition-all"
            aria-label={t("header.nav.home")}
        >
            <motion.div
                whileHover={{scale: 1.01}}
                whileTap={{scale: 0.99}}
                className="flex items-center gap-3"
            >
                <img src={petallogo} alt="Mimir Logo" className="h-15 w-auto"/>

                {/* Text container (stacked) */}
                <div className="hidden sm:flex flex-col leading-tight">
          <span className="text-xl font-bold tracking-tight text-base-content">
            PETAL
            </span>
                    {isAuthenticated && realm && (
                        <span className="text-sm text-base-content/70">
              {realm}
            </span>
                    )}
                </div>
            </motion.div>
        </Link>
    );
})