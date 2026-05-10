import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { createElement } from 'react';
import { ModelApiProvider } from '../ModelApiProvider';
import { ApiBasePathContext } from '../../../contexts/api/apiBasePathContext';
import { ModelApiContext } from '../../../contexts/api/modelApiContext';

vi.mock('../../../config/axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
}));

vi.mock('@isin/model-service-client', () => ({
    Configuration: vi.fn().mockImplementation(function (this: object, opts: object) {
        Object.assign(this, opts);
    }),
    AdaptersApi: vi.fn().mockImplementation(function (this: object) {
        Object.assign(this, { _type: 'AdaptersApi' });
    }),
}));

function TestConsumer() {
    return (
        <ModelApiContext.Consumer>
            {(value) => (
                <span data-testid="adapters-api">{value?.adaptersApi ? 'present' : 'absent'}</span>
            )}
        </ModelApiContext.Consumer>
    );
}

function renderProvider(basePath = '') {
    return render(
        createElement(ApiBasePathContext.Provider, { value: { basePath } },
            <ModelApiProvider>
                <TestConsumer />
            </ModelApiProvider>)
    );
}

describe('ModelApiProvider', () => {
    it('provides adaptersApi to consumers', () => {
        renderProvider();
        expect(screen.getByTestId('adapters-api').textContent).toBe('present');
    });

    it('renders children', () => {
        renderProvider();
        expect(screen.getByTestId('adapters-api')).toBeTruthy();
    });

    it('creates Configuration with the provided basePath', async () => {
        const { Configuration } = await import('@isin/model-service-client');
        renderProvider('http://model-base');
        expect(vi.mocked(Configuration)).toHaveBeenCalledWith(
            expect.objectContaining({ basePath: 'http://model-base' })
        );
    });

    it('recreates APIs when basePath changes', () => {
        const { rerender } = renderProvider('http://base-1');
        rerender(
            createElement(ApiBasePathContext.Provider, { value: { basePath: 'http://base-2' } },
                <ModelApiProvider>
                    <TestConsumer />
                </ModelApiProvider>)
        );
        expect(screen.getByTestId('adapters-api').textContent).toBe('present');
    });
});
