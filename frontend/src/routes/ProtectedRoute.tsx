import { Navigate } from "react-router-dom";
import type {ReactNode} from "react";
import {useAuthWrapper} from "../hooks/auth/useAuthWrapper.ts";

type ProtectedRouteProps = {
    children: ReactNode;
    departmentAdminOnly?: boolean
};

export const ProtectedRoute = ({ children, departmentAdminOnly = false }: ProtectedRouteProps) => {
    const { isAuthenticated, isLoading, isDepartmentAdmin } = useAuthWrapper();

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <span className="loading loading-spinner loading-lg"></span>
            </div>
        );
    }

    if (!isAuthenticated || (departmentAdminOnly && !isDepartmentAdmin) ) {
        return <Navigate to="/" replace />;
    }

    return <>{children}</>;
};