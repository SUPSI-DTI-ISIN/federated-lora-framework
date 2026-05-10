import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useCreateInstitute } from '../useCreateInstitute';

vi.mock('../../../../config/instituteServiceClient', () => ({
    instituteApi: {
        createInstituteApiInstituteInstitutesPost: vi.fn(),
    },
}));

import { instituteApi } from '../../../../config/instituteServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children) };
}

describe('useCreateInstitute', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with name and url', async () => {
        const newInstitute = { id: 10, name: 'New', url: 'http://new.local' };
        vi.mocked(instituteApi.createInstituteApiInstituteInstitutesPost).mockResolvedValue({ data: newInstitute } as never);

        const { queryClient, wrapper } = createWrapper();
        queryClient.setQueryData(['institutes'], []);

        const { result } = renderHook(() => useCreateInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ name: 'New', url: 'http://new.local' });
        });

        expect(instituteApi.createInstituteApiInstituteInstitutesPost).toHaveBeenCalledWith({ name: 'New', url: 'http://new.local' });
    });

    it('appends the new institute to the cache on success', async () => {
        const existing = [{ id: 1, name: 'Old', url: 'http://old.local' }];
        const newInstitute = { id: 2, name: 'New', url: 'http://new.local' };
        vi.mocked(instituteApi.createInstituteApiInstituteInstitutesPost).mockResolvedValue({ data: newInstitute } as never);

        const { queryClient, wrapper } = createWrapper();
        queryClient.setQueryData(['institutes'], existing);

        const { result } = renderHook(() => useCreateInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ name: 'New', url: 'http://new.local' });
        });

        const cached = queryClient.getQueryData<typeof existing>(['institutes']);
        expect(cached).toHaveLength(2);
        expect(cached?.[1]).toEqual(newInstitute);
    });

    it('creates a new list when cache is empty', async () => {
        const newInstitute = { id: 1, name: 'First', url: 'http://first.local' };
        vi.mocked(instituteApi.createInstituteApiInstituteInstitutesPost).mockResolvedValue({ data: newInstitute } as never);

        const { queryClient, wrapper } = createWrapper();

        const { result } = renderHook(() => useCreateInstitute(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ name: 'First', url: 'http://first.local' });
        });

        const cached = queryClient.getQueryData(['institutes']);
        expect(cached).toEqual([newInstitute]);
    });
});
