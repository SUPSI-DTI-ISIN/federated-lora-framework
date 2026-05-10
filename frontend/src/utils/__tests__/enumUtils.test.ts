import { describe, it, expect } from 'vitest';
import { formatEnum } from '../enumUtils';

describe('formatEnum', () => {
    it('converts lowercase string to uppercase', () => {
        expect(formatEnum('active')).toBe('ACTIVE');
    });

    it('replaces underscores with spaces', () => {
        expect(formatEnum('in_progress')).toBe('IN PROGRESS');
    });

    it('handles multiple underscores', () => {
        expect(formatEnum('very_long_status_name')).toBe('VERY LONG STATUS NAME');
    });

    it('returns empty string when input is empty', () => {
        expect(formatEnum('')).toBe('');
    });

    it('handles already uppercase string', () => {
        expect(formatEnum('SUCCESS')).toBe('SUCCESS');
    });

    it('handles mixed case with underscores', () => {
        expect(formatEnum('In_Progress')).toBe('IN PROGRESS');
    });

    it('handles single word', () => {
        expect(formatEnum('pending')).toBe('PENDING');
    });
});
