interface LoadingSkeletonProps {
  variant: 'list' | 'card' | 'table';
  count?: number;
}

/**
 * LoadingSkeleton Component
 * 
 * A reusable loading skeleton component that displays loading states matching the layout structure of loaded content.
 * 
 * Features:
 * - Supports variants for list, card, and table layouts
 * - Uses DaisyUI skeleton component with theme-appropriate colors
 * - Configurable count of skeleton items to display
 * - Matches the structure of actual content for smooth transitions
 * - Uses Design_System colors and spacing
 * 
 * Requirements satisfied:
 * - 16.4: Provide LoadingSkeleton reusable component
 * - 16.11: Pure presentation component without business logic
 * - 17.1: Render Loading_State using DaisyUI skeleton loaders
 * - 17.2: Match layout structure of loaded content
 * - 17.7: Use Design_System colors and spacing
 * 
 * @example
 * ```tsx
 * // List variant
 * <LoadingSkeleton variant="list" count={5} />
 * 
 * // Card variant
 * <LoadingSkeleton variant="card" count={3} />
 * 
 * // Table variant
 * <LoadingSkeleton variant="table" count={4} />
 * ```
 */
export function LoadingSkeleton({
  variant,
  count = 3,
}: LoadingSkeletonProps) {
  const items = Array.from({ length: count }, (_, i) => i);

  if (variant === 'list') {
    return (
      <div className="space-y-3" role="status" aria-label="Loading content">
        {items.map((i) => (
          <div
            key={i}
            className="flex items-center gap-4 rounded-lg bg-base-100 p-4 shadow"
          >
            {/* Icon/Avatar skeleton */}
            <div className="h-10 w-10 flex-shrink-0 animate-pulse rounded-full bg-base-300" />
            
            {/* Content skeleton */}
            <div className="flex-1 space-y-2">
              <div className="h-4 w-3/4 animate-pulse rounded bg-base-300" />
              <div className="h-3 w-1/2 animate-pulse rounded bg-base-300" />
            </div>
            
            {/* Action skeleton */}
            <div className="h-8 w-20 flex-shrink-0 animate-pulse rounded bg-base-300" />
          </div>
        ))}
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  if (variant === 'card') {
    return (
      <div
        className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
        role="status"
        aria-label="Loading content"
      >
        {items.map((i) => (
          <div
            key={i}
            className="card bg-base-100 shadow-md"
          >
            <div className="card-body p-6">
              {/* Title skeleton */}
              <div className="mb-3 h-5 w-3/4 animate-pulse rounded bg-base-300" />
              
              {/* Badge skeleton */}
              <div className="mb-4 h-6 w-20 animate-pulse rounded-full bg-base-300" />
              
              {/* Description skeleton */}
              <div className="space-y-2">
                <div className="h-3 w-full animate-pulse rounded bg-base-300" />
                <div className="h-3 w-5/6 animate-pulse rounded bg-base-300" />
              </div>
              
              {/* Actions skeleton */}
              <div className="card-actions mt-4 justify-end gap-2">
                <div className="h-8 w-16 animate-pulse rounded-lg bg-base-300" />
                <div className="h-8 w-16 animate-pulse rounded-lg bg-base-300" />
              </div>
            </div>
          </div>
        ))}
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  if (variant === 'table') {
    return (
      <div
        className="overflow-x-auto rounded-lg bg-base-100 shadow"
        role="status"
        aria-label="Loading content"
      >
        <table className="table w-full">
          <thead>
            <tr>
              <th>
                <div className="h-4 w-24 animate-pulse rounded bg-base-300" />
              </th>
              <th>
                <div className="h-4 w-20 animate-pulse rounded bg-base-300" />
              </th>
              <th>
                <div className="h-4 w-16 animate-pulse rounded bg-base-300" />
              </th>
              <th>
                <div className="h-4 w-16 animate-pulse rounded bg-base-300" />
              </th>
              <th>
                <div className="h-4 w-20 animate-pulse rounded bg-base-300" />
              </th>
            </tr>
          </thead>
          <tbody>
            {items.map((i) => (
              <tr key={i}>
                <td>
                  <div className="flex items-center gap-3">
                    <div className="h-8 w-8 flex-shrink-0 animate-pulse rounded bg-base-300" />
                    <div className="h-4 w-32 animate-pulse rounded bg-base-300" />
                  </div>
                </td>
                <td>
                  <div className="h-6 w-16 animate-pulse rounded-full bg-base-300" />
                </td>
                <td>
                  <div className="h-4 w-20 animate-pulse rounded bg-base-300" />
                </td>
                <td>
                  <div className="h-4 w-16 animate-pulse rounded bg-base-300" />
                </td>
                <td>
                  <div className="flex gap-2">
                    <div className="h-8 w-8 animate-pulse rounded-lg bg-base-300" />
                    <div className="h-8 w-8 animate-pulse rounded-lg bg-base-300" />
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  return null;
}
