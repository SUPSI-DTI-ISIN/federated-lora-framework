import {AuthWrapperProvider} from "./AuthWrapperProvider.tsx";
import type {ReactNode} from "react";
import {AuthProvider} from "react-oidc-context";
import {getOidcAuthConfiguration} from "../../auth/auth.ts";
import {useSelectorRealm} from "../../hooks/realm/useSelectorRealm.ts";

interface AuthProvidersProps {
    children: ReactNode;
}

export const AuthProviders = ({children}: AuthProvidersProps) => {
    const {realm} = useSelectorRealm();

    return (
        <AuthProvider {...getOidcAuthConfiguration(realm)}>
            <AuthWrapperProvider>
                {children}
            </AuthWrapperProvider>
        </AuthProvider>
    )
}