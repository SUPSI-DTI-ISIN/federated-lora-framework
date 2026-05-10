import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useGetInstituteByName } from '../useGetInstituteByName';

vi.mock('../../../../config/instituteServiceClient', () => ({
    instituteApi: {
        getInstituteByNameApiInstituteInstitutesNameInstituteNameGet: vi.fn(),
    },
}));

import { instituteApi } from '../../../../config/instituteServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children);
}

describe('useGetInstituteByName', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns institute when name is provided', async () => {
        const institute = { id: 1, name: 'Alpha', url: 'http://alpha.local' };
        vi.mocked(instituteApi.getInstituteByNameApiInstituteInstitutesNameInstituteNameGet).mockResolvedValue({ data: institute } as never);

        const { result } = renderHook(() => useGetInstituteByName('Alpha'), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(institute);
    });

    it('does not fetch when instituteName is undefined', () => {
        const { result } = renderHook(() => useGetInstituteByName(undefined), { wrapper: createWrapper() });

        expect(result.current.fetchStatus).toBe('idle');
        expect(instituteApi.getInstituteByNameApiInstituteInstitutesNameInstituteNameGet).not.toHaveBeenCalled();
    });

    it('sets error state on failure', async () => {
        vi.mocked(instituteApi.getInstituteByNameApiInstituteInstitutesNameInstituteNameGet).mockRejectedValue(new Error('Not found'));

        const { result } = renderHook(() => useGetInstituteByName('Ghost'), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
