import {useSelectorRealm} from "../hooks/realm/useSelectorRealm.ts";

export const RealmsPage = () => {
    const {realm, setRealm} = useSelectorRealm();

    console.log(realm);

    return (
        <>
        </>
    )
}