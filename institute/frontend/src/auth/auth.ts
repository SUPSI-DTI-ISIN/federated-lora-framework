import {getClientId, getFrontendUrl, getInstituteName, getKeycloakUrl} from "../utils/envUtils.ts";
import type {AuthProviderProps} from "react-oidc-context";
import {WebStorageStateStore} from "oidc-client-ts";

export const getOidcAuthConfiguration = (): AuthProviderProps => {
    return {
        authority: `${getKeycloakUrl()}/realms/${getInstituteName()}`,
        client_id: getClientId(),
        redirect_uri: `${getFrontendUrl()}`,
        response_type: "code",
        scope: "openid profile email",
        post_logout_redirect_uri: `${getFrontendUrl()}`,
        userStore: new WebStorageStateStore({ store: window.localStorage }),
        onSigninCallback: () => {
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    };
}