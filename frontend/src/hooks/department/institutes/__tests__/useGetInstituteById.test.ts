import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useGetInstituteById } from '../useGetInstituteById';

vi.mock('../../../../config/instituteServiceClient', () => ({
    instituteApi: {
        getInstituteByIdApiInstituteInstitutesInstituteIdGet: vi.fn(),
    },
}));

import { instituteApi } from '../../../../config/instituteServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children);
}

describe('useGetInstituteById', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns institute on success', async () => {
        const institute = { id: 5, name: 'Inst', url: 'http://inst.local' };
        vi.mocked(instituteApi.getInstituteByIdApiInstituteInstitutesInstituteIdGet).mockResolvedValue({ data: institute } as never);

        const { result } = renderHook(() => useGetInstituteById(5), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(institute);
    });

    it('calls the API with the correct instituteId', async () => {
        vi.mocked(instituteApi.getInstituteByIdApiInstituteInstitutesInstituteIdGet).mockResolvedValue({ data: {} } as never);

        const { result } = renderHook(() => useGetInstituteById(42), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(instituteApi.getInstituteByIdApiInstituteInstitutesInstituteIdGet).toHaveBeenCalledWith(42);
    });

    it('sets error state on failure', async () => {
        vi.mocked(instituteApi.getInstituteByIdApiInstituteInstitutesInstituteIdGet).mockRejectedValue(new Error('Not found'));

        const { result } = renderHook(() => useGetInstituteById(99), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
