import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ModelApiContext } from '../../../../contexts/api/modelApiContext';
import { createElement } from 'react';
import { useSaveNewAdapter } from '../useSaveNewAdapter';

type AdapterDTO = { version: number; available_local: boolean };
type AvailableAdaptersDTO = { model_key: string; adapters: AdapterDTO[] | null | undefined };

function createWrapper(adaptersApi: { saveNewAdapterApiModelModelsModelKeyAdaptersPost: ReturnType<typeof vi.fn> }) {
    const queryClient = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const contextValue = { adaptersApi: adaptersApi as never };
    return { queryClient, wrapper: ({ children }: { children: React.ReactNode }) =>
        createElement(QueryClientProvider, { client: queryClient },
            createElement(ModelApiContext.Provider, { value: contextValue }, children)) };
}

describe('useSaveNewAdapter', () => {
    beforeEach(() => vi.clearAllMocks());

    it('calls the API with modelKey and adapterVersion', async () => {
        const newAdapter: AdapterDTO = { version: 3, available_local: true };
        const adaptersApi = { saveNewAdapterApiModelModelsModelKeyAdaptersPost: vi.fn().mockResolvedValue({ data: newAdapter }) };

        const { wrapper } = createWrapper(adaptersApi);
        const { result } = renderHook(() => useSaveNewAdapter(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ modelKey: 'llama-3', adapterVersion: 3 });
        });

        expect(adaptersApi.saveNewAdapterApiModelModelsModelKeyAdaptersPost).toHaveBeenCalledWith('llama-3', { version: 3 });
    });

    it('updates the adapter in the adapters cache when it exists', async () => {
        const existing: AvailableAdaptersDTO = { model_key: 'llama-3', adapters: [{ version: 3, available_local: false }] };
        const newAdapter: AdapterDTO = { version: 3, available_local: true };
        const adaptersApi = { saveNewAdapterApiModelModelsModelKeyAdaptersPost: vi.fn().mockResolvedValue({ data: newAdapter }) };

        const { queryClient, wrapper } = createWrapper(adaptersApi);
        queryClient.setQueryData(['adapters'], existing);

        const { result } = renderHook(() => useSaveNewAdapter(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ modelKey: 'llama-3', adapterVersion: 3 });
        });

        const cached = queryClient.getQueryData<AvailableAdaptersDTO>(['adapters']);
        expect(cached?.adapters?.[0].available_local).toBe(true);
    });

    it('creates a new adapters list when cache has no adapters', async () => {
        const newAdapter: AdapterDTO = { version: 1, available_local: true };
        const adaptersApi = { saveNewAdapterApiModelModelsModelKeyAdaptersPost: vi.fn().mockResolvedValue({ data: newAdapter }) };

        const { queryClient, wrapper } = createWrapper(adaptersApi);
        queryClient.setQueryData(['adapters'], { model_key: 'llama-3', adapters: null });

        const { result } = renderHook(() => useSaveNewAdapter(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ modelKey: 'llama-3', adapterVersion: 1 });
        });

        const cached = queryClient.getQueryData<AvailableAdaptersDTO>(['adapters']);
        expect(cached?.adapters).toEqual([newAdapter]);
    });

    it('invalidates local adapters query on success', async () => {
        const newAdapter: AdapterDTO = { version: 1, available_local: true };
        const adaptersApi = { saveNewAdapterApiModelModelsModelKeyAdaptersPost: vi.fn().mockResolvedValue({ data: newAdapter }) };

        const { queryClient, wrapper } = createWrapper(adaptersApi);
        const invalidateSpy = vi.spyOn(queryClient, 'invalidateQueries');

        const { result } = renderHook(() => useSaveNewAdapter(), { wrapper });

        await act(async () => {
            await result.current.mutateAsync({ modelKey: 'llama-3', adapterVersion: 1 });
        });

        expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ['adapters', 'local'] });
    });
});
