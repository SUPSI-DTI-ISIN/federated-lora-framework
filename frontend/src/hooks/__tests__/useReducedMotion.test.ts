import {describe, it, expect, vi, beforeEach, afterEach} from 'vitest';
import {renderHook, act} from '@testing-library/react';
import {useReducedMotion} from '../useReducedMotion';

const mockAddEventListener = vi.fn();
const mockRemoveEventListener = vi.fn();

function mockMatchMedia(matches: boolean) {
    return vi.fn().mockImplementation(() => ({
        matches,
        addEventListener: mockAddEventListener,
        removeEventListener: mockRemoveEventListener,
    }));
}

describe('useReducedMotion', () => {
    beforeEach(() => {
        mockAddEventListener.mockClear();
        mockRemoveEventListener.mockClear();
        window.matchMedia = mockMatchMedia(false);
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('returns false when prefers-reduced-motion does not match', () => {
        window.matchMedia = mockMatchMedia(false);
        const {result} = renderHook(() => useReducedMotion());
        expect(result.current).toBe(false);
    });

    it('returns true when prefers-reduced-motion matches', () => {
        window.matchMedia = mockMatchMedia(true);
        const {result} = renderHook(() => useReducedMotion());
        expect(result.current).toBe(true);
    });

    it('adds a change event listener on mount', () => {
        renderHook(() => useReducedMotion());
        expect(mockAddEventListener).toHaveBeenCalledWith('change', expect.any(Function));
    });

    it('removes the change event listener on unmount', () => {
        const {unmount} = renderHook(() => useReducedMotion());
        unmount();
        expect(mockRemoveEventListener).toHaveBeenCalledWith('change', expect.any(Function));
    });

    it('updates state when media query change event fires', () => {
        let capturedHandler: ((e: MediaQueryListEvent) => void) | null = null;
        window.matchMedia = vi.fn().mockImplementation(() => ({
            matches: false,
            addEventListener: (_: string, handler: (e: MediaQueryListEvent) => void) => {
                capturedHandler = handler;
            },
            removeEventListener: mockRemoveEventListener,
        }));

        const {result} = renderHook(() => useReducedMotion());
        expect(result.current).toBe(false);

        act(() => {
            capturedHandler?.({matches: true} as MediaQueryListEvent);
        });

        expect(result.current).toBe(true);
    });

    it('returns false as initial state when matchMedia is unavailable', () => {
        vi.spyOn(window, 'matchMedia').mockImplementation(() => {
            throw new Error('matchMedia not available');
        });

        const {result} = renderHook(() => {
            try {
                return useReducedMotion();
            } catch {
                return false;
            }
        });

        expect(result.current).toBe(false);
    });
});
