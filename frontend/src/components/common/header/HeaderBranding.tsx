import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { motion } from "framer-motion";
import mimirLogo from "../../../assets/mimir-logo.png";

export function HeaderBranding() {
  const { t } = useTranslation();

  return (
    <Link
      to="/"
      className="group flex items-center gap-3 focus-visible:outline-primary rounded-lg transition-all"
      aria-label={t("header.nav.home")}
    >
      <motion.div whileHover={{ scale: 1.01 }} whileTap={{ scale: 0.99 }} className="flex items-center gap-3">
        <img src={mimirLogo} alt="Mimir Logo" className="h-10 w-auto" />
        <span className="hidden text-xl font-bold tracking-tight text-base-content sm:inline-block">
          {t("header.title")}
        </span>
      </motion.div>
    </Link>
  );
}
