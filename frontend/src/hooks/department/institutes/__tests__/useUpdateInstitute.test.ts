import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useUpdateInstitute } from '../useUpdateInstitute';

vi.mock('../../../../config/instituteServiceClient', () => ({
    instituteApi: {
        updateInstituteApiInstituteInstitutesInstituteIdPut: vi.fn(),
    },
}));

import { instituteApi } from '../../../../config/instituteServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children) };
}

describe('useUpdateInstitute', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with correct params', async () => {
        const updated = { id: 1, name: 'Updated', url: 'http://updated.local' };
        vi.mocked(instituteApi.updateInstituteApiInstituteInstitutesInstituteIdPut).mockResolvedValue({ data: updated } as never);

        const { wrapper } = createWrapper();
        const { result } = renderHook(() => useUpdateInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ instituteId: 1, updateInstituteBody: { name: 'Updated', url: 'http://updated.local' } });
        });

        expect(instituteApi.updateInstituteApiInstituteInstitutesInstituteIdPut).toHaveBeenCalledWith(1, { name: 'Updated', url: 'http://updated.local' });
    });

    it('updates the institute in the cache', async () => {
        const existing = [{ id: 1, name: 'Old', url: 'http://old.local' }, { id: 2, name: 'Other', url: 'http://other.local' }];
        const updated = { id: 1, name: 'New', url: 'http://new.local' };
        vi.mocked(instituteApi.updateInstituteApiInstituteInstitutesInstituteIdPut).mockResolvedValue({ data: updated } as never);

        const { queryClient, wrapper } = createWrapper();
        queryClient.setQueryData(['institutes'], existing);

        const { result } = renderHook(() => useUpdateInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ instituteId: 1, updateInstituteBody: { name: 'New' } });
        });

        const cached = queryClient.getQueryData<typeof existing>(['institutes']);
        expect(cached?.[0]).toEqual(updated);
        expect(cached?.[1]).toEqual(existing[1]);
    });

    it('creates a list with the updated institute when cache is empty', async () => {
        const updated = { id: 1, name: 'New', url: 'http://new.local' };
        vi.mocked(instituteApi.updateInstituteApiInstituteInstitutesInstituteIdPut).mockResolvedValue({ data: updated } as never);

        const { queryClient, wrapper } = createWrapper();
        const { result } = renderHook(() => useUpdateInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ instituteId: 1, updateInstituteBody: { name: 'New' } });
        });

        expect(queryClient.getQueryData(['institutes'])).toEqual([updated]);
    });
});
