import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('../axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
}));

describe('mlflowServiceClient', () => {
    beforeEach(() => {
        vi.resetModules();
        vi.doMock('@isin/mlflow-service-client', () => ({
            Configuration: vi.fn().mockImplementation(function (this: object, opts: object) {
                Object.assign(this, opts);
            }),
            AdapterApi: vi.fn().mockImplementation(function (this: object) {
                Object.assign(this, { _isAdapterApi: true });
            }),
        }));
    });

    it('exports departmentAdaptersApi', async () => {
        const { departmentAdaptersApi } = await import('../mlflowServiceClient');
        expect(departmentAdaptersApi).toBeDefined();
    });

    it('AdapterApi is constructed once', async () => {
        const { AdapterApi } = await import('@isin/mlflow-service-client');
        await import('../mlflowServiceClient');
        expect(AdapterApi).toHaveBeenCalledOnce();
    });

    it('Configuration is called with empty basePath', async () => {
        const { Configuration } = await import('@isin/mlflow-service-client');
        await import('../mlflowServiceClient');
        const callArg = vi.mocked(Configuration).mock.calls[0]?.[0] as { basePath: string };
        expect(callArg?.basePath).toBe('');
    });
});
