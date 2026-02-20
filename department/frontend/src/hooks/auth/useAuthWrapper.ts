import {useContext} from "react";
import {AuthWrapperContext} from "../../contexts/auth/authWrapperContext.ts";

export const useAuthWrapper = () => {
    const context = useContext(AuthWrapperContext);
    if (!context) {
        throw new Error("useAuthWrapper must be used within AuthWrapperProvider");
    }
    return context;
}