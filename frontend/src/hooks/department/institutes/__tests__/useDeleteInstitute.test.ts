import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useDeleteInstitute } from '../useDeleteInstitute';

vi.mock('../../../../config/instituteServiceClient', () => ({
    instituteApi: {
        deleteInstituteApiInstituteInstitutesInstituteIdDelete: vi.fn(),
    },
}));

import { instituteApi } from '../../../../config/instituteServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children) };
}

describe('useDeleteInstitute', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with the correct instituteId', async () => {
        vi.mocked(instituteApi.deleteInstituteApiInstituteInstitutesInstituteIdDelete).mockResolvedValue({ data: undefined } as never);

        const { wrapper } = createWrapper();
        const { result } = renderHook(() => useDeleteInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        expect(instituteApi.deleteInstituteApiInstituteInstitutesInstituteIdDelete).toHaveBeenCalledWith(1);
    });

    it('removes the deleted institute from the cache', async () => {
        const institutes = [{ id: 1, name: 'A' }, { id: 2, name: 'B' }];
        vi.mocked(instituteApi.deleteInstituteApiInstituteInstitutesInstituteIdDelete).mockResolvedValue({ data: undefined } as never);

        const { queryClient, wrapper } = createWrapper();
        queryClient.setQueryData(['institutes'], institutes);

        const { result } = renderHook(() => useDeleteInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        const cached = queryClient.getQueryData<typeof institutes>(['institutes']);
        expect(cached).toHaveLength(1);
        expect(cached?.[0].id).toBe(2);
    });

    it('returns undefined when cache is empty', async () => {
        vi.mocked(instituteApi.deleteInstituteApiInstituteInstitutesInstituteIdDelete).mockResolvedValue({ data: undefined } as never);

        const { queryClient, wrapper } = createWrapper();
        const { result } = renderHook(() => useDeleteInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync(1);
        });

        expect(queryClient.getQueryData(['institutes'])).toBeUndefined();
    });
});
