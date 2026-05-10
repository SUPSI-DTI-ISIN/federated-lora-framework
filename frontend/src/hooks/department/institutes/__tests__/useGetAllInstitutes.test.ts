import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useGetAllInstitutes } from '../useGetAllInstitutes';

vi.mock('../../../../config/instituteServiceClient', () => ({
    instituteApi: {
        listInstitutesApiInstituteInstitutesGet: vi.fn(),
    },
}));

import { instituteApi } from '../../../../config/instituteServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({
        defaultOptions: { queries: { retry: false } },
    });
    return ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children);
}

describe('useGetAllInstitutes', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('returns institutes on success', async () => {
        const institutes = [{ id: 1, name: 'Inst A', url: 'http://a.local' }];
        vi.mocked(instituteApi.listInstitutesApiInstituteInstitutesGet).mockResolvedValue({
            data: institutes,
        } as never);

        const { result } = renderHook(() => useGetAllInstitutes(), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(institutes);
    });

    it('uses the correct query key', async () => {
        vi.mocked(instituteApi.listInstitutesApiInstituteInstitutesGet).mockResolvedValue({
            data: [],
        } as never);

        const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
        const wrapper = ({ children }: { children: React.ReactNode }) =>
            createElement(QueryClientProvider, { client: queryClient }, children);

        renderHook(() => useGetAllInstitutes(), { wrapper });

        await waitFor(() =>
            expect(queryClient.getQueryState(['institutes'])).toBeDefined()
        );
    });

    it('sets error state on failure', async () => {
        vi.mocked(instituteApi.listInstitutesApiInstituteInstitutesGet).mockRejectedValue(
            new Error('Network error')
        );

        const { result } = renderHook(() => useGetAllInstitutes(), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isError).toBe(true));
        expect(result.current.error?.message).toBe('Network error');
    });
});
