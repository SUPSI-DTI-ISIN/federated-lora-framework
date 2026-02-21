import {useContext} from "react";
import {SelectorRealmContext} from "../../contexts/realm/selectorRealmContext.ts";

export const useSelectorRealm = () => {
    const context = useContext(SelectorRealmContext);
    if (!context) {
        throw new Error("useSelectorRealm must be used within SelectorRealmContext");
    }
    return context;
}