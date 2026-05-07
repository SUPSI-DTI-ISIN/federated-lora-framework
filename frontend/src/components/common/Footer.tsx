import { useTranslation } from "react-i18next";
import { FaGithub, FaLinkedin, FaInstagram, FaHeart, FaCode } from "react-icons/fa";
import { motion } from "framer-motion";
import petallogo from '../../assets/petal-logo.png';

export const Footer = () => {
    const { t } = useTranslation();
    const currentYear = new Date().getFullYear();

    const contactData = {
        name: "Luca Fantò",
        instagram: "https://instagram.com/luca_fanto_",
        role: t('footer.role'),
        github: "https://github.com/lucafanto",
        linkedin: "https://www.linkedin.com/in/luca-fant%C3%B2-14197232a/",
    };

    return (
        <footer className="relative border-t border-base-content/10 bg-base-100/90 backdrop-blur-md py-12">
            <div className="container mx-auto px-6">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-16 items-center">

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        className="flex flex-col gap-6"
                    >
                        <h4 className="text-2xl font-black tracking-tight bg-linear-to-r from-primary to-secondary bg-clip-text text-transparent">
                            {t("footer.about.title")}
                        </h4>
                        <p className="text-lg leading-relaxed text-base-content/80 max-w-md">
                            {t("footer.about.description")}
                        </p>
                    </motion.div>

                    <motion.div
                        className="flex flex-col items-center gap-8"
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.1 }}
                    >
                            <img
                                src={petallogo}
                                alt="Mimir Logo"
                                className="h-25 w-auto object-contain drop-shadow-xl transition-all group-hover:drop-shadow-2xl"
                            />

                        <div className="flex flex-col items-center gap-4">
                            <div className="flex items-center gap-3 text-lg font-semibold text-base-content/80">
                                <span>{t('footer.craftedWith')}</span>
                                <motion.span
                                    animate={{ scale: [1, 1.2, 1] }}
                                    transition={{ repeat: Infinity, duration: 2 }}
                                >
                                    <FaHeart className="text-error" />
                                </motion.span>
                                <span>{t('footer.and')}</span>
                                <FaCode className="text-primary" />
                            </div>

                            <div className="text-base-content/50 text-sm font-medium tracking-widest uppercase">
                                &copy; {currentYear} PETAL
                            </div>
                        </div>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ delay: 0.2 }}
                        className="flex flex-col lg:items-end gap-6"
                    >
                        <div className="bg-base-200/40 p-6 rounded-2xl border border-base-content/5 w-full max-w-sm lg:text-center">
                            <div className="mb-4">
                                <p className="text-xl font-bold text-base-content">{contactData.name}</p>
                                <p className="text-primary font-semibold text-sm tracking-wide uppercase">{contactData.role}</p>
                            </div>

                            <div className="flex gap-3 lg:justify-center">
                                {[
                                    { href: contactData.github, icon: FaGithub, label: "GitHub" },
                                    { href: contactData.linkedin, icon: FaLinkedin, label: "LinkedIn" },
                                    { href: contactData.instagram, icon: FaInstagram, label: "Instagram" }
                                ].map((social, idx) => (
                                    <a
                                        key={idx}
                                        href={social.href}
                                        target="_blank"
                                        rel="noreferrer"
                                        aria-label={social.label}
                                        className="group relative flex h-12 w-12 items-center justify-center rounded-xl bg-base-100 shadow-sm transition-all duration-300 hover:bg-primary hover:-translate-y-1 hover:shadow-lg hover:shadow-primary/30"
                                    >
                                        <social.icon
                                            size={22}
                                            className="text-base-content transition-colors group-hover:text-primary-content"
                                        />
                                    </a>
                                ))}
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>
        </footer>
    );
};