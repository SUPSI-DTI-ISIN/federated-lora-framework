import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('../axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
}));

describe('instituteServiceClient', () => {
    beforeEach(() => {
        vi.resetModules();
        vi.doMock('@isin/institute-service-client', () => ({
            Configuration: vi.fn().mockImplementation(function (this: object, opts: object) {
                Object.assign(this, opts);
            }),
            InstituteApi: vi.fn().mockImplementation(function (this: object) {
                Object.assign(this, { _isInstituteApi: true });
            }),
        }));
    });

    it('exports instituteApi', async () => {
        const { instituteApi } = await import('../instituteServiceClient');
        expect(instituteApi).toBeDefined();
    });

    it('InstituteApi is constructed once', async () => {
        const { InstituteApi } = await import('@isin/institute-service-client');
        await import('../instituteServiceClient');
        expect(InstituteApi).toHaveBeenCalledOnce();
    });

    it('Configuration is called with empty basePath', async () => {
        const { Configuration } = await import('@isin/institute-service-client');
        await import('../instituteServiceClient');
        const callArg = vi.mocked(Configuration).mock.calls[0]?.[0] as { basePath: string };
        expect(callArg?.basePath).toBe('');
    });
});
