import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { createElement } from 'react';
import { ApiProviders } from '../ApiProviders';
import { SelectorRealmContext } from '../../../contexts/realm/selectorRealmContext';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

vi.mock('../../../utils/envUtils', () => ({
    isInDevelopmentEnvironment: vi.fn().mockReturnValue(true),
    getDepartmentRealm: vi.fn().mockReturnValue('Department'),
}));

vi.mock('../../../hooks/department/institutes/useGetInstituteByName', () => ({
    useGetInstituteByName: vi.fn().mockReturnValue({ data: undefined, isLoading: false }),
}));

vi.mock('../../../config/axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
}));

vi.mock('@isin/chat-service-client', () => ({
    Configuration: vi.fn().mockImplementation(function (this: object) {}),
    ChatApi: vi.fn().mockImplementation(function (this: object) {}),
    MessagesApi: vi.fn().mockImplementation(function (this: object) {}),
}));

vi.mock('@isin/data-service-client', () => ({
    Configuration: vi.fn().mockImplementation(function (this: object) {}),
    DocumentsApi: vi.fn().mockImplementation(function (this: object) {}),
    SectionsApi: vi.fn().mockImplementation(function (this: object) {}),
}));

vi.mock('@isin/model-service-client', () => ({
    Configuration: vi.fn().mockImplementation(function (this: object) {}),
    AdaptersApi: vi.fn().mockImplementation(function (this: object) {}),
}));

vi.mock('react-icons/cg', () => ({
    CgSpinner: () => <div data-testid="spinner" />,
}));

function renderProviders(children: React.ReactNode) {
    const queryClient = new QueryClient();
    const realmValue = { realm: 'Department', setRealm: vi.fn(), pendingLogin: false, clearPendingLogin: vi.fn() };

    return render(
        createElement(QueryClientProvider, { client: queryClient },
            createElement(SelectorRealmContext.Provider, { value: realmValue },
                <ApiProviders>{children}</ApiProviders>))
    );
}

describe('ApiProviders', () => {
    it('renders children', () => {
        renderProviders(<div data-testid="child">Child</div>);
        expect(screen.getByTestId('child')).toBeTruthy();
    });

    it('wraps children with all API providers', () => {
        renderProviders(<div data-testid="child">Child</div>);
        expect(screen.getByText('Child')).toBeTruthy();
    });

    it('renders without crashing', () => {
        expect(() => renderProviders(<span>test</span>)).not.toThrow();
    });
});
