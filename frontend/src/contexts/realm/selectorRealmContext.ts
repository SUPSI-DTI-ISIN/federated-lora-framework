import {createContext} from "react";

export type SelectorRealmContext = {
    realm: string | undefined;
    setRealm: (realm?: string) => void;
    pendingLogin: boolean;
    clearPendingLogin: () => void;
};

export const SelectorRealmContext = createContext<SelectorRealmContext | undefined>(undefined);
