import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { SelectorRealmProvider } from '../SelectorRealmProvider';
import { useSelectorRealm } from '../../../hooks/realm/useSelectorRealm';

function TestConsumer() {
    const { realm, setRealm, pendingLogin, clearPendingLogin } = useSelectorRealm();
    return (
        <div>
            <span data-testid="realm">{realm ?? 'none'}</span>
            <span data-testid="pending">{String(pendingLogin)}</span>
            <button onClick={() => setRealm('TestRealm')}>Set Realm</button>
            <button onClick={() => setRealm(undefined)}>Clear Realm</button>
            <button onClick={clearPendingLogin}>Clear Pending</button>
        </div>
    );
}

function renderProvider() {
    return render(
        <SelectorRealmProvider>
            <TestConsumer />
        </SelectorRealmProvider>
    );
}

describe('SelectorRealmProvider', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        vi.stubGlobal('localStorage', {
            getItem: vi.fn().mockReturnValue(null),
            setItem: vi.fn(),
            removeItem: vi.fn(),
            clear: vi.fn(),
        });
    });

    afterEach(() => {
        vi.unstubAllGlobals();
    });

    it('provides undefined realm by default when localStorage is empty', () => {
        renderProvider();
        expect(screen.getByTestId('realm').textContent).toBe('none');
    });

    it('initialises realm from localStorage', () => {
        vi.stubGlobal('localStorage', {
            getItem: vi.fn().mockReturnValue('StoredRealm'),
            setItem: vi.fn(),
            removeItem: vi.fn(),
        });
        renderProvider();
        expect(screen.getByTestId('realm').textContent).toBe('StoredRealm');
    });

    it('initialises pendingLogin as true when localStorage has realm', () => {
        vi.stubGlobal('localStorage', {
            getItem: vi.fn().mockReturnValue('StoredRealm'),
            setItem: vi.fn(),
            removeItem: vi.fn(),
        });
        renderProvider();
        expect(screen.getByTestId('pending').textContent).toBe('true');
    });

    it('initialises pendingLogin as false when localStorage is empty', () => {
        renderProvider();
        expect(screen.getByTestId('pending').textContent).toBe('false');
    });

    it('sets realm and stores it in localStorage', () => {
        const mockSetItem = vi.fn();
        vi.stubGlobal('localStorage', {
            getItem: vi.fn().mockReturnValue(null),
            setItem: mockSetItem,
            removeItem: vi.fn(),
        });
        renderProvider();
        fireEvent.click(screen.getByText('Set Realm'));
        expect(screen.getByTestId('realm').textContent).toBe('TestRealm');
        expect(mockSetItem).toHaveBeenCalledWith('selected-realm', 'TestRealm');
    });

    it('sets pendingLogin to true when realm is set', () => {
        renderProvider();
        fireEvent.click(screen.getByText('Set Realm'));
        expect(screen.getByTestId('pending').textContent).toBe('true');
    });

    it('clears realm and removes it from localStorage', () => {
        const mockRemoveItem = vi.fn();
        vi.stubGlobal('localStorage', {
            getItem: vi.fn().mockReturnValue('TestRealm'),
            setItem: vi.fn(),
            removeItem: mockRemoveItem,
        });
        renderProvider();
        fireEvent.click(screen.getByText('Clear Realm'));
        expect(screen.getByTestId('realm').textContent).toBe('none');
        expect(mockRemoveItem).toHaveBeenCalledWith('selected-realm');
    });

    it('sets pendingLogin to false when realm is cleared', () => {
        vi.stubGlobal('localStorage', {
            getItem: vi.fn().mockReturnValue('TestRealm'),
            setItem: vi.fn(),
            removeItem: vi.fn(),
        });
        renderProvider();
        fireEvent.click(screen.getByText('Clear Realm'));
        expect(screen.getByTestId('pending').textContent).toBe('false');
    });

    it('clearPendingLogin sets pendingLogin to false', () => {
        renderProvider();
        fireEvent.click(screen.getByText('Set Realm'));
        expect(screen.getByTestId('pending').textContent).toBe('true');
        fireEvent.click(screen.getByText('Clear Pending'));
        expect(screen.getByTestId('pending').textContent).toBe('false');
    });

    it('renders children', () => {
        renderProvider();
        expect(screen.getByTestId('realm')).toBeTruthy();
    });
});
