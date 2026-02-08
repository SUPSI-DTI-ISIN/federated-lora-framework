import { Navigate } from "react-router-dom";
import type {ReactNode} from "react";
import {useAuthWrapper} from "../hooks/auth/useAuthWrapper.ts";

type ProtectedRouteProps = {
    children: ReactNode;
};

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const { isAuthenticated, isLoading } = useAuthWrapper();

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <span className="loading loading-spinner loading-lg"></span>
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/" replace />;
    }

    return <>{children}</>;
};