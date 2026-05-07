import {createContext} from "react";
import type {User} from "oidc-client-ts";

export type AuthWrapperContextType = {
    user: User | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    isDepartmentAdmin: boolean;
    login: () => void;
    logout: () => void;
};

export const AuthWrapperContext = createContext<AuthWrapperContextType | undefined>(undefined);
