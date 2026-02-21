import {type ReactNode, useMemo} from "react";
import {useSelectorRealm} from "../../hooks/realm/useSelectorRealm.ts";
import {useGetInstituteByName} from "../../hooks/department/institutes/useGetInstituteByName.ts";
import {isInDevelopmentEnvironment} from "../../utils/envUtils.ts";
import {ApiBasePathContext} from "../../contexts/api/apiBasePathContext.ts";

interface ApiBasePathProviderProps {
    children: ReactNode;
}

export const ApiBasePathProvider = ({children}: ApiBasePathProviderProps) => {
    const {realm} = useSelectorRealm();
    const {data: institute} = useGetInstituteByName(realm);

    const basePath = useMemo(() => ({
        basePath: isInDevelopmentEnvironment() ? "" : (institute?.url ?? "")
    }), [institute?.url]);

    return (
        <ApiBasePathContext.Provider value={basePath}>
            {children}
        </ApiBasePathContext.Provider>
    );
};