import { describe, it, expect, beforeEach } from 'vitest';
import { axiosInstance, setAuthToken } from '../axios';

describe('axiosInstance', () => {
    it('is an axios instance', () => {
        expect(axiosInstance).toBeDefined();
        expect(typeof axiosInstance.get).toBe('function');
        expect(typeof axiosInstance.post).toBe('function');
    });
});

describe('setAuthToken', () => {
    beforeEach(() => {
        delete axiosInstance.defaults.headers.common['Authorization'];
    });

    it('sets the Authorization header when token is provided', () => {
        setAuthToken('my-token');
        expect(axiosInstance.defaults.headers.common['Authorization']).toBe('Bearer my-token');
    });

    it('removes the Authorization header when token is null', () => {
        setAuthToken('initial-token');
        setAuthToken(null);
        expect(axiosInstance.defaults.headers.common['Authorization']).toBeUndefined();
    });

    it('updates the Authorization header when called again with a new token', () => {
        setAuthToken('first-token');
        setAuthToken('second-token');
        expect(axiosInstance.defaults.headers.common['Authorization']).toBe('Bearer second-token');
    });
});
