import {type ReactNode, useCallback, useEffect, useMemo, useState} from "react";
import {hasAuthParams, useAuth} from "react-oidc-context";
import {AuthWrapperContext} from "../../contexts/auth/authWrapperContext.ts";
import {setAuthToken} from "../../config/axios.ts";
import {useQueryClient} from "@tanstack/react-query";
import {useSelectorRealm} from "../../hooks/realm/useSelectorRealm.ts";

interface AuthWrapperProviderProps {
    children: ReactNode;
}

export const AuthWrapperProvider = ({children}: AuthWrapperProviderProps) => {
    const auth = useAuth();
    const queryClient = useQueryClient();
    const {realm, setRealm, pendingLogin, clearPendingLogin} = useSelectorRealm();
    const [hasTriedSignin, setHasTriedSignin] = useState(false);

    const isLoading = useMemo(() => {
        const authBusy =
            auth.activeNavigator === "signinRedirect" ||
            auth.activeNavigator === "signinSilent" ||
            auth.activeNavigator === "signoutRedirect";
        return auth.isLoading || authBusy;
    }, [auth.isLoading, auth.activeNavigator]);

    useEffect(() => {
        setAuthToken(auth.user?.access_token ?? null);
        queryClient.invalidateQueries();
    }, [auth.user?.access_token, queryClient]);

    useEffect(() => {
        if (auth.error) {
            clearPendingLogin();
            setRealm(undefined);
            setHasTriedSignin(true);
        }
    }, [auth.error, clearPendingLogin, setRealm]);

    useEffect(() => {
        if (auth.isLoading || auth.activeNavigator) return;
        if (pendingLogin && !auth.user) {
            clearPendingLogin();
            auth.signinRedirect();
            return;
        }

        if (!pendingLogin && !auth.user && !hasTriedSignin && !hasAuthParams()) {
            setHasTriedSignin(true);
            auth.signinSilent().catch(() => {});
        }
    }, [pendingLogin, auth.isLoading, auth.activeNavigator, auth.user, hasTriedSignin, clearPendingLogin, auth.error]);

    const login = useCallback(async () => {
        try {
            console.log("login");
            await auth.signinRedirect();
        } catch (err) {
            console.error("Login failed:", err);
            throw err;
        }
    }, [auth]);

    const logout = useCallback(async () => {
        try {
            setAuthToken(null);
            setRealm(undefined);
            await auth.signoutRedirect();
        } catch (err) {
            auth.removeUser();
            console.error("Logout failed:", err);
            throw err;
        }
    }, [auth, setRealm]);

    const value = useMemo(() => ({
            user: auth.user ?? null,
            isLoading,
            isAuthenticated: auth.isAuthenticated && !!auth.user && !!auth.user.profile && !!realm,
            isDepartmentAdmin: auth.isAuthenticated && !!auth.user && !!auth.user.profile && !!realm && auth.user?.profile?.realm_admin === true,
            login,
            logout,
        }),
        [auth.user, isLoading, auth.isAuthenticated, login, logout, realm]
    );

    return (
        <AuthWrapperContext.Provider value={value}>
            {children}
        </AuthWrapperContext.Provider>
    );
};
