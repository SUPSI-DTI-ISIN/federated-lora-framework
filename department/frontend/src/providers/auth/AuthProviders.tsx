import {AuthWrapperProvider} from "./AuthWrapperProvider.tsx";
import type {ReactNode} from "react";
import {AuthProvider} from "react-oidc-context";
import {getOidcAuthConfiguration} from "../../auth/auth.ts";

interface AuthProvidersProps {
    children: ReactNode;
}

export const AuthProviders = ({children}: AuthProvidersProps) => {
    return (
        <AuthProvider {...getOidcAuthConfiguration()}>
            <AuthWrapperProvider>
                {children}
            </AuthWrapperProvider>
        </AuthProvider>
    )
}