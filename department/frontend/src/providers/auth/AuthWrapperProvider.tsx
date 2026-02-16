import {type ReactNode, useCallback, useEffect, useMemo, useState} from "react";
import {hasAuthParams, useAuth} from "react-oidc-context";
import {AuthWrapperContext} from "../../contexts/auth/authWrapperContext.ts";
import {setAuthToken} from "../../config/axios.ts";
import {useQueryClient} from "@tanstack/react-query";

interface AuthWrapperProviderProps {
    children: ReactNode;
}

export const AuthWrapperProvider = ({children}: AuthWrapperProviderProps) => {
    const auth = useAuth();
    const queryClient = useQueryClient();
    const [hasTriedSignin, setHasTriedSignin] = useState(false);

    const isLoading = useMemo(() => {
        const authBusy =
            auth.activeNavigator === "signinRedirect" ||
            auth.activeNavigator === "signinSilent" ||
            auth.activeNavigator === "signoutRedirect";
        return auth.isLoading || authBusy;
    }, [auth.isLoading, auth.activeNavigator]);

    useEffect(() => {
        const token = auth.user?.access_token ?? null;
        setAuthToken(token);
        queryClient.invalidateQueries();
    }, [auth.user?.access_token, queryClient]);

    useEffect(() => {
        if (
            !hasAuthParams() &&
            !auth.user &&
            !auth.activeNavigator &&
            !auth.isLoading &&
            !hasTriedSignin
        ) {
            auth.signinSilent()
                .catch(() => {})
                .finally(() => {
                    setHasTriedSignin(true);
                });
        }
    }, [auth, hasTriedSignin]);

    const login = useCallback(async () => {
        try {
            await auth.signinRedirect();
        } catch (err) {
            console.error("Login failed:", err);
            throw err;
        }
    }, [auth]);

    const logout = useCallback(async () => {
        try {
            setAuthToken(null);

            await auth.signoutRedirect();
        } catch (err) {
            auth.removeUser();
            console.error("Logout failed:", err);
            throw err;
        }
    }, [auth]);

    const value = useMemo(() => ({
            user: auth.user ?? null,
            isLoading,
            isAuthenticated: auth.isAuthenticated && !!auth.user && !!auth.user.profile,
            login,
            logout,
        }),
        [auth.user, isLoading, auth.isAuthenticated, login, logout]
    );

    return (
        <AuthWrapperContext.Provider value={value}>
            {children}
        </AuthWrapperContext.Provider>
    );
};
