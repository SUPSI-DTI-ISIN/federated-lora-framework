export const getModelKey = (): string => {
    return import.meta.env.VITE_MODEL_KEY;
}

export const getKeycloakUrl = (): string => {
    return import.meta.env.VITE_KEYCLOAK_URL;
}

export const getFrontendUrl = (): string => {
    return import.meta.env.VITE_FRONTEND_URL;
}

export const getClientId = (): string => {
    return import.meta.env.VITE_CLIENT_ID;
}