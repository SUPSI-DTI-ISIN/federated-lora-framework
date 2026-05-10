import { describe, it, expect, vi, beforeEach } from 'vitest';

describe('i18n', () => {
    beforeEach(() => {
        vi.resetModules();
    });

    it('initialises i18next and exports the instance', async () => {
        const initMock = vi.fn().mockReturnThis();
        const useMock = vi.fn().mockReturnThis();

        vi.doMock('i18next', () => ({ default: { use: useMock, init: initMock } }));
        vi.doMock('i18next-browser-languagedetector', () => ({ default: class LanguageDetector {} }));
        vi.doMock('react-i18next', () => ({ initReactI18next: {} }));
        vi.doMock('../locales/en/translations.json', () => ({ default: { hello: 'Hello' } }));
        vi.doMock('../locales/it/translations.json', () => ({ default: { hello: 'Ciao' } }));

        const module = await import('../i18n');
        expect(module.default).toBeDefined();
        expect(useMock).toHaveBeenCalled();
        expect(initMock).toHaveBeenCalled();
    });

    it('configures fallback language as en', async () => {
        const initMock = vi.fn().mockReturnThis();
        vi.doMock('i18next', () => ({ default: { use: vi.fn().mockReturnThis(), init: initMock } }));
        vi.doMock('i18next-browser-languagedetector', () => ({ default: class LanguageDetector {} }));
        vi.doMock('react-i18next', () => ({ initReactI18next: {} }));
        vi.doMock('../locales/en/translations.json', () => ({ default: {} }));
        vi.doMock('../locales/it/translations.json', () => ({ default: {} }));

        await import('../i18n');
        const initArg = initMock.mock.calls[0]?.[0] as { fallbackLng: string };
        expect(initArg?.fallbackLng).toBe('en');
    });

    it('configures supported languages including en and it', async () => {
        const initMock = vi.fn().mockReturnThis();
        vi.doMock('i18next', () => ({ default: { use: vi.fn().mockReturnThis(), init: initMock } }));
        vi.doMock('i18next-browser-languagedetector', () => ({ default: class LanguageDetector {} }));
        vi.doMock('react-i18next', () => ({ initReactI18next: {} }));
        vi.doMock('../locales/en/translations.json', () => ({ default: {} }));
        vi.doMock('../locales/it/translations.json', () => ({ default: {} }));

        await import('../i18n');
        const initArg = initMock.mock.calls[0]?.[0] as { supportedLngs: string[] };
        expect(initArg?.supportedLngs).toContain('en');
        expect(initArg?.supportedLngs).toContain('it');
    });

    it('disables debug mode', async () => {
        const initMock = vi.fn().mockReturnThis();
        vi.doMock('i18next', () => ({ default: { use: vi.fn().mockReturnThis(), init: initMock } }));
        vi.doMock('i18next-browser-languagedetector', () => ({ default: class LanguageDetector {} }));
        vi.doMock('react-i18next', () => ({ initReactI18next: {} }));
        vi.doMock('../locales/en/translations.json', () => ({ default: {} }));
        vi.doMock('../locales/it/translations.json', () => ({ default: {} }));

        await import('../i18n');
        const initArg = initMock.mock.calls[0]?.[0] as { debug: boolean };
        expect(initArg?.debug).toBe(false);
    });

    it('disables escapeValue in interpolation', async () => {
        const initMock = vi.fn().mockReturnThis();
        vi.doMock('i18next', () => ({ default: { use: vi.fn().mockReturnThis(), init: initMock } }));
        vi.doMock('i18next-browser-languagedetector', () => ({ default: class LanguageDetector {} }));
        vi.doMock('react-i18next', () => ({ initReactI18next: {} }));
        vi.doMock('../locales/en/translations.json', () => ({ default: {} }));
        vi.doMock('../locales/it/translations.json', () => ({ default: {} }));

        await import('../i18n');
        const initArg = initMock.mock.calls[0]?.[0] as { interpolation: { escapeValue: boolean } };
        expect(initArg?.interpolation?.escapeValue).toBe(false);
    });

    it('includes en and it resources', async () => {
        const initMock = vi.fn().mockReturnThis();
        vi.doMock('i18next', () => ({ default: { use: vi.fn().mockReturnThis(), init: initMock } }));
        vi.doMock('i18next-browser-languagedetector', () => ({ default: class LanguageDetector {} }));
        vi.doMock('react-i18next', () => ({ initReactI18next: {} }));
        vi.doMock('../locales/en/translations.json', () => ({ default: { hello: 'Hello' } }));
        vi.doMock('../locales/it/translations.json', () => ({ default: { hello: 'Ciao' } }));

        await import('../i18n');
        const initArg = initMock.mock.calls[0]?.[0] as { resources: Record<string, unknown> };
        expect(Object.keys(initArg?.resources ?? {})).toContain('en');
        expect(Object.keys(initArg?.resources ?? {})).toContain('it');
    });
});
