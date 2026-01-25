import { useTranslation } from "react-i18next";
import { FaGithub, FaLinkedin, FaMailBulk } from "react-icons/fa";

export const Footer = () => {
    const { t } = useTranslation();
    const currentYear = new Date().getFullYear();

    return (
        <footer className="border-t border-base-300 bg-base-100/60">
            <div className="max-w-7xl mx-auto px-4 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {/* About */}
                    <div>
                        <h4 className="font-semibold text-lg mb-2">{t("footer.about.title")}</h4>
                        <p className="text-sm text-base-content/70">{t("footer.about.description")}</p>
                    </div>

                    {/* Links */}
                    <div>
                        <h4 className="font-semibold text-lg mb-2">{t("footer.links.title")}</h4>
                        <ul className="text-sm space-y-2">
                            <li>
                                <a href="#" className="link link-hover text-base-content/70 hover:text-primary">
                                    {t("footer.links.documentation")}
                                </a>
                            </li>
                            <li>
                                <a href="#" className="link link-hover text-base-content/70 hover:text-primary">
                                    {t("footer.links.support")}
                                </a>
                            </li>
                            <li>
                                <a href="#" className="link link-hover text-base-content/70 hover:text-primary">
                                    {t("footer.links.privacy")}
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Contact / Social */}
                    <div>
                        <h4 className="font-semibold text-lg mb-2">{t("footer.contact.title")}</h4>
                        <p className="text-sm text-base-content/70 mb-3">{t("footer.contact.description")}</p>
                        <div className="flex gap-3">
                            <a
                                href="#"
                                className="btn btn-ghost btn-circle btn-sm"
                                aria-label={t("footer.contact.github") as string}
                            >
                                <FaGithub size={18} />
                            </a>
                            <a
                                href="#"
                                className="btn btn-ghost btn-circle btn-sm"
                                aria-label={t("footer.contact.linkedin") as string}
                            >
                                <FaLinkedin size={18} />
                            </a>
                            <a
                                href="#"
                                className="btn btn-ghost btn-circle btn-sm"
                                aria-label={t("footer.contact.email") as string}
                            >
                                <FaMailBulk size={18} />
                            </a>
                        </div>
                    </div>
                </div>

                <div className="divider my-6"></div>

                <div className="text-center text-sm text-base-content/60">
                    <p>
                        © {currentYear} {t("footer.copyright")}
                    </p>
                </div>
            </div>
        </footer>
    );
};