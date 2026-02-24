import {type ReactNode, useCallback, useMemo, useState} from "react";
import {SelectorRealmContext} from "../../contexts/realm/selectorRealmContext.ts";

interface SelectorRealmProviderProps {
    children: ReactNode;
}

export const SelectorRealmProvider = ({children}: SelectorRealmProviderProps) => {
    const [selectedRealm, setSelectedRealm] = useState<string | undefined>(() => {
        return localStorage.getItem("selected-realm") ?? undefined;
    });
    const [pendingLogin, setPendingLogin] = useState(false);

    const setRealm = useCallback((realm: string | undefined) => {
        setSelectedRealm(realm);
        if (realm) {
            localStorage.setItem("selected-realm", realm);
            setPendingLogin(true);
        } else {
            localStorage.removeItem("selected-realm");
            setPendingLogin(false);
        }
    }, []);

    const clearPendingLogin = useCallback(() => setPendingLogin(false), []);

    const value = useMemo(() => ({
        realm: selectedRealm,
        setRealm,
        pendingLogin,
        clearPendingLogin
    }), [selectedRealm, setRealm, pendingLogin, clearPendingLogin]);

    return (
        <SelectorRealmContext.Provider value={value}>
            {children}
        </SelectorRealmContext.Provider>
    );
};