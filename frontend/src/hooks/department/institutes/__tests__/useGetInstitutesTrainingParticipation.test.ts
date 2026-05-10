import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { createElement } from 'react';
import { useGetInstitutesTrainingParticipation } from '../useGetInstitutesTrainingParticipation';

vi.mock('../../../../config/instituteServiceClient', () => ({
    instituteApi: {
        getInstitutesTrainingParticipationApiInstituteInstitutesTrainingParticipationGet: vi.fn(),
    },
}));

import { instituteApi } from '../../../../config/instituteServiceClient';

function createWrapper() {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    return ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient }, children);
}

describe('useGetInstitutesTrainingParticipation', () => {
    beforeEach(() => vi.clearAllMocks());

    it('returns participation data on success', async () => {
        const data = [{ id: 1, institute_name: 'Alpha', trainable_samples_number: 10, is_reachable: true }];
        vi.mocked(instituteApi.getInstitutesTrainingParticipationApiInstituteInstitutesTrainingParticipationGet).mockResolvedValue({ data } as never);

        const { result } = renderHook(() => useGetInstitutesTrainingParticipation(), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isSuccess).toBe(true));
        expect(result.current.data).toEqual(data);
    });

    it('sets error state on failure', async () => {
        vi.mocked(instituteApi.getInstitutesTrainingParticipationApiInstituteInstitutesTrainingParticipationGet).mockRejectedValue(new Error('fail'));

        const { result } = renderHook(() => useGetInstitutesTrainingParticipation(), { wrapper: createWrapper() });

        await waitFor(() => expect(result.current.isError).toBe(true));
    });
});
