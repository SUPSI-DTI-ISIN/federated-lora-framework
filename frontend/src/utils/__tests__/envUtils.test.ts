import { describe, it, expect } from 'vitest';

describe('envUtils', () => {
    it('getModelKey returns a string', async () => {
        const { getModelKey } = await import('../envUtils');
        expect(typeof getModelKey()).toBe('string');
    });

    it('getKeycloakUrl returns a string', async () => {
        const { getKeycloakUrl } = await import('../envUtils');
        expect(typeof getKeycloakUrl()).toBe('string');
    });

    it('getFlowerCeleryJobsUrl returns a string', async () => {
        const { getFlowerCeleryJobsUrl } = await import('../envUtils');
        expect(typeof getFlowerCeleryJobsUrl()).toBe('string');
    });

    it('getFrontendUrl returns a string', async () => {
        const { getFrontendUrl } = await import('../envUtils');
        expect(typeof getFrontendUrl()).toBe('string');
    });

    it('getClientId returns a string', async () => {
        const { getClientId } = await import('../envUtils');
        expect(typeof getClientId()).toBe('string');
    });

    it('getDepartmentRealm returns a string', async () => {
        const { getDepartmentRealm } = await import('../envUtils');
        expect(typeof getDepartmentRealm()).toBe('string');
    });

    it('isInDevelopmentEnvironment returns a boolean', async () => {
        const { isInDevelopmentEnvironment } = await import('../envUtils');
        expect(typeof isInDevelopmentEnvironment()).toBe('boolean');
    });

    it('isInDevelopmentEnvironment returns true only for development or dev environments', async () => {
        const { isInDevelopmentEnvironment } = await import('../envUtils');
        const env = import.meta.env.VITE_ENVIRONMENT as string | undefined;
        const expected = env === 'development' || env === 'dev';
        expect(isInDevelopmentEnvironment()).toBe(expected);
    });

    it('getModelKey reads from VITE_MODEL_KEY', async () => {
        const { getModelKey } = await import('../envUtils');
        expect(getModelKey()).toBe(import.meta.env.VITE_MODEL_KEY);
    });

    it('getKeycloakUrl reads from VITE_KEYCLOAK_URL', async () => {
        const { getKeycloakUrl } = await import('../envUtils');
        expect(getKeycloakUrl()).toBe(import.meta.env.VITE_KEYCLOAK_URL);
    });

    it('getFrontendUrl reads from VITE_FRONTEND_URL', async () => {
        const { getFrontendUrl } = await import('../envUtils');
        expect(getFrontendUrl()).toBe(import.meta.env.VITE_FRONTEND_URL);
    });

    it('getClientId reads from VITE_CLIENT_ID', async () => {
        const { getClientId } = await import('../envUtils');
        expect(getClientId()).toBe(import.meta.env.VITE_CLIENT_ID);
    });

    it('getDepartmentRealm reads from VITE_DEPARTMENT_REALM', async () => {
        const { getDepartmentRealm } = await import('../envUtils');
        expect(getDepartmentRealm()).toBe(import.meta.env.VITE_DEPARTMENT_REALM);
    });

    it('getFlowerCeleryJobsUrl reads from VITE_FLOWER_CELERY_JOBS_URL', async () => {
        const { getFlowerCeleryJobsUrl } = await import('../envUtils');
        expect(getFlowerCeleryJobsUrl()).toBe(import.meta.env.VITE_FLOWER_CELERY_JOBS_URL);
    });
});
