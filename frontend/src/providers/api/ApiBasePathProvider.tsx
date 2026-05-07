import { type ReactNode, useMemo } from "react";
import { useSelectorRealm } from "../../hooks/realm/useSelectorRealm.ts";
import { useGetInstituteByName } from "../../hooks/department/institutes/useGetInstituteByName.ts";
import {getDepartmentRealm, isInDevelopmentEnvironment} from "../../utils/envUtils.ts";
import { ApiBasePathContext } from "../../contexts/api/apiBasePathContext.ts";
import {CgSpinner} from "react-icons/cg";

interface ApiBasePathProviderProps {
    children: ReactNode;
}

export const ApiBasePathProvider = ({ children }: ApiBasePathProviderProps) => {
    const { realm } = useSelectorRealm();
    const { data: institute, isLoading: isLoadingInstitute } = useGetInstituteByName(realm);

    const basePath = useMemo(() => {
        if (isInDevelopmentEnvironment() || !realm || realm === getDepartmentRealm()) return "";
        return institute?.url ?? null;
    }, [institute]);

    const value = useMemo(() => ({ basePath: basePath ?? "" }), [basePath]);

    if ( realm !== getDepartmentRealm() && (isLoadingInstitute || basePath === null)) {
        return <div className="flex flex-1 items-center justify-center">
            <CgSpinner />
        </div>;
    }

    return (
        <ApiBasePathContext.Provider value={value}>
            {children}
        </ApiBasePathContext.Provider>
    );
};