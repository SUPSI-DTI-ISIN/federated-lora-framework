import { useTranslation } from 'react-i18next';
import {FaGithub, FaLinkedin, FaMailBulk} from "react-icons/fa";

export const Footer = () => {
    const { t } = useTranslation();
    const currentYear = new Date().getFullYear();

    return (
        <footer className="bg-base-300 text-base-content mt-auto">
            <div className="max-w-7xl mx-auto px-4 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {/* About Section */}
                    <div>
                        <h3 className="font-bold text-lg mb-3">{t('footer.about.title')}</h3>
                        <p className="text-sm text-base-content/70">
                            {t('footer.about.description')}
                        </p>
                    </div>

                    {/* Quick Links */}
                    <div>
                        <h3 className="font-bold text-lg mb-3">{t('footer.links.title')}</h3>
                        <ul className="text-sm space-y-2">
                            <li>
                                <a href="#" className="link link-hover text-base-content/70 hover:text-primary">
                                    {t('footer.links.documentation')}
                                </a>
                            </li>
                            <li>
                                <a href="#" className="link link-hover text-base-content/70 hover:text-primary">
                                    {t('footer.links.support')}
                                </a>
                            </li>
                            <li>
                                <a href="#" className="link link-hover text-base-content/70 hover:text-primary">
                                    {t('footer.links.privacy')}
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Contact */}
                    <div>
                        <h3 className="font-bold text-lg mb-3">{t('footer.contact.title')}</h3>
                        <div className="flex gap-4">
                            <a href="#" className="btn btn-circle btn-ghost btn-sm hover:bg-primary hover:text-primary-content">
                                <FaGithub size={20} />
                            </a>
                            <a href="#" className="btn btn-circle btn-ghost btn-sm hover:bg-primary hover:text-primary-content">
                                <FaLinkedin size={20} />
                            </a>
                            <a href="#" className="btn btn-circle btn-ghost btn-sm hover:bg-primary hover:text-primary-content">
                                <FaMailBulk size={20} />
                            </a>
                        </div>
                    </div>
                </div>

                <div className="divider"></div>

                <div className="text-center text-sm text-base-content/60">
                    <p>
                        © {currentYear} {t('footer.copyright')} | {t('footer.masterThesis')}
                    </p>
                </div>
            </div>
        </footer>
    );
};