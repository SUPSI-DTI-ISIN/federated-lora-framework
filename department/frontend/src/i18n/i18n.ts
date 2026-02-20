import i18n from 'i18next'
import LanguageDetector from "i18next-browser-languagedetector";
import {initReactI18next} from "react-i18next";

import translations_en from './locales/en/translations.json';
import translations_it from './locales/it/translations.json';

i18n.use(LanguageDetector).use(initReactI18next).init({
    fallbackLng: 'en',
    debug: false,
    supportedLngs: ['it', 'en'],
    detection: {
        order: ['localStorage', 'navigator'],
        caches: ['localStorage'],
    },
    resources: {
        en: {
            translation: translations_en
        },
        it: {
            translation: translations_it
        },
    },

    interpolation:{
        escapeValue: false,
    },
});

export default i18n;