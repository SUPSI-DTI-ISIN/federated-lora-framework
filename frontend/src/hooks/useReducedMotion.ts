import { useEffect, useState } from 'react';

/**
 * useReducedMotion Hook
 * 
 * Detects if the user has enabled the "prefers-reduced-motion" accessibility setting.
 * This hook respects user preferences for reduced motion and should be used to
 * disable or reduce animations when the user has this preference enabled.
 * 
 * Requirements satisfied:
 * - 10.7: Respect prefers-reduced-motion media query
 * - 10.8: Disable or reduce animations when prefers-reduced-motion is set
 * - 19.9: Motion system respects prefers-reduced-motion preference
 * 
 * @returns {boolean} true if user prefers reduced motion, false otherwise
 * 
 * @example
 * ```tsx
 * const prefersReducedMotion = useReducedMotion();
 * 
 * <motion.div
 *   animate={prefersReducedMotion ? {} : { opacity: 1, y: 0 }}
 *   transition={prefersReducedMotion ? { duration: 0 } : { duration: 0.3 }}
 * >
 *   Content
 * </motion.div>
 * ```
 */
export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState<boolean>(
    () => {
      // Check on initial render
      if (typeof window === 'undefined') return false;
      const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
      return mediaQuery.matches;
    }
  );

  useEffect(() => {
    // Create media query
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    // Update state when preference changes
    const handleChange = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    // Listen for changes
    mediaQuery.addEventListener('change', handleChange);

    // Cleanup
    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }, []);

  return prefersReducedMotion;
}
