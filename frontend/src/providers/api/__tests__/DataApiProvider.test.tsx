import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { createElement } from 'react';
import { DataApiProvider } from '../DataApiProvider';
import { ApiBasePathContext } from '../../../contexts/api/apiBasePathContext';
import { DataApiContext } from '../../../contexts/api/dataApiContext';

vi.mock('../../../config/axios', () => ({
    axiosInstance: { defaults: { headers: { common: {} } } },
}));

vi.mock('@isin/data-service-client', () => ({
    Configuration: vi.fn().mockImplementation(function (this: object, opts: object) {
        Object.assign(this, opts);
    }),
    DocumentsApi: vi.fn().mockImplementation(function (this: object) {
        Object.assign(this, { _type: 'DocumentsApi' });
    }),
    SectionsApi: vi.fn().mockImplementation(function (this: object) {
        Object.assign(this, { _type: 'SectionsApi' });
    }),
}));

function TestConsumer() {
    return (
        <DataApiContext.Consumer>
            {(value) => (
                <div>
                    <span data-testid="documents-api">{value?.documentsApi ? 'present' : 'absent'}</span>
                    <span data-testid="sections-api">{value?.sectionsApi ? 'present' : 'absent'}</span>
                </div>
            )}
        </DataApiContext.Consumer>
    );
}

function renderProvider(basePath = '') {
    return render(
        createElement(ApiBasePathContext.Provider, { value: { basePath } },
            <DataApiProvider>
                <TestConsumer />
            </DataApiProvider>)
    );
}

describe('DataApiProvider', () => {
    it('provides documentsApi to consumers', () => {
        renderProvider();
        expect(screen.getByTestId('documents-api').textContent).toBe('present');
    });

    it('provides sectionsApi to consumers', () => {
        renderProvider();
        expect(screen.getByTestId('sections-api').textContent).toBe('present');
    });

    it('renders children', () => {
        renderProvider();
        expect(screen.getByTestId('documents-api')).toBeTruthy();
    });

    it('creates Configuration with the provided basePath', async () => {
        const { Configuration } = await import('@isin/data-service-client');
        renderProvider('http://data-base');
        expect(vi.mocked(Configuration)).toHaveBeenCalledWith(
            expect.objectContaining({ basePath: 'http://data-base' })
        );
    });

    it('recreates APIs when basePath changes', () => {
        const { rerender } = renderProvider('http://base-1');
        rerender(
            createElement(ApiBasePathContext.Provider, { value: { basePath: 'http://base-2' } },
                <DataApiProvider>
                    <TestConsumer />
                </DataApiProvider>)
        );
        expect(screen.getByTestId('documents-api').textContent).toBe('present');
    });
});
