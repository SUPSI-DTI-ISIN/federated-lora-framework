export const getModelKey = (): string => {
    return import.meta.env.VITE_MODEL_KEY;
}

export const getInstituteName = (): string => {
    return import.meta.env.VITE_INSTITUTE_NAME;
}

export const getAuthAuthority = (): string => {
    return import.meta.env.VITE_AUTH_AUTHORITY;
}

export const getFrontendUrl = (): string => {
    return import.meta.env.VITE_FRONTEND_URL;
}

export const getClientId = (): string => {
    return import.meta.env.VITE_CLIENT_ID;
}