export const getModelKey = (): string => {
    return import.meta.env.VITE_MODEL_KEY;
}

export const getKeycloakUrl = (): string => {
    return import.meta.env.VITE_KEYCLOAK_URL;
}

export const getFlowerCeleryJobsUrl = (): string => {
    return import.meta.env.VITE_FLOWER_CELERY_JOBS_URL;
}

export const getFrontendUrl = (): string => {
    return import.meta.env.VITE_FRONTEND_URL;
}

export const getClientId = (): string => {
    return import.meta.env.VITE_CLIENT_ID;
}

const getEnvironment = (): string => {
    return import.meta.env.VITE_ENVIRONMENT;
}

export const isInDevelopmentEnvironment = (): boolean => {
    return getEnvironment() === "development" || getEnvironment() === "dev"
}