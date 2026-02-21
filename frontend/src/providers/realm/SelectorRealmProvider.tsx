import {type ReactNode, useMemo, useState} from "react";
import {SelectorRealmContext} from "../../contexts/realm/selectorRealmContext.ts";

interface SelectorRealmProviderProps {
    children: ReactNode;
}

export const SelectorRealmProvider = ({children}: SelectorRealmProviderProps) => {
    const [selectedRealm, setSelectedRealm] = useState<string | undefined>(undefined);


    const value = useMemo(() => ({
            realm: selectedRealm,
            setRealm: setSelectedRealm,
        }),
        [selectedRealm, setSelectedRealm]
    );

    return (
        <SelectorRealmContext.Provider value={value}>
            {children}
        </SelectorRealmContext.Provider>
    );
};
