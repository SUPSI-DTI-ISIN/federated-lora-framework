import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { ProtectedRoute } from '../ProtectedRoute';
import { AuthWrapperContext } from '../../contexts/auth/authWrapperContext';
import { createElement } from 'react';

vi.mock('react-router-dom', async () => {
    const actual = await vi.importActual<typeof import('react-router-dom')>('react-router-dom');
    return { ...actual, Navigate: vi.fn(({ to }: { to: string }) => <div data-testid="navigate" data-to={to} />) };
});

function renderWithAuth(
    ui: React.ReactNode,
    auth: { isAuthenticated: boolean; isLoading: boolean; isDepartmentAdmin: boolean }
) {
    const value = { ...auth, user: null, login: vi.fn(), logout: vi.fn() };
    return render(
        createElement(AuthWrapperContext.Provider, { value },
            createElement(MemoryRouter, {}, ui))
    );
}

describe('ProtectedRoute', () => {
    it('renders a loading spinner while loading', () => {
        renderWithAuth(
            <ProtectedRoute><div>Protected</div></ProtectedRoute>,
            { isAuthenticated: false, isLoading: true, isDepartmentAdmin: false }
        );
        expect(document.querySelector('.loading')).toBeTruthy();
        expect(screen.queryByText('Protected')).toBeNull();
    });

    it('renders children when authenticated', () => {
        renderWithAuth(
            <ProtectedRoute><div>Protected Content</div></ProtectedRoute>,
            { isAuthenticated: true, isLoading: false, isDepartmentAdmin: false }
        );
        expect(screen.getByText('Protected Content')).toBeTruthy();
    });

    it('redirects to / when not authenticated', () => {
        renderWithAuth(
            <ProtectedRoute><div>Protected</div></ProtectedRoute>,
            { isAuthenticated: false, isLoading: false, isDepartmentAdmin: false }
        );
        expect(screen.getByTestId('navigate').getAttribute('data-to')).toBe('/');
        expect(screen.queryByText('Protected')).toBeNull();
    });

    it('redirects to / when departmentAdminOnly and user is not admin', () => {
        renderWithAuth(
            <ProtectedRoute departmentAdminOnly><div>Admin Only</div></ProtectedRoute>,
            { isAuthenticated: true, isLoading: false, isDepartmentAdmin: false }
        );
        expect(screen.getByTestId('navigate').getAttribute('data-to')).toBe('/');
    });

    it('renders children when departmentAdminOnly and user is admin', () => {
        renderWithAuth(
            <ProtectedRoute departmentAdminOnly><div>Admin Content</div></ProtectedRoute>,
            { isAuthenticated: true, isLoading: false, isDepartmentAdmin: true }
        );
        expect(screen.getByText('Admin Content')).toBeTruthy();
    });

    it('defaults departmentAdminOnly to false', () => {
        renderWithAuth(
            <ProtectedRoute><div>Default Route</div></ProtectedRoute>,
            { isAuthenticated: true, isLoading: false, isDepartmentAdmin: false }
        );
        expect(screen.getByText('Default Route')).toBeTruthy();
    });
});
