interface StatusBadgeProps {
  status: string;
  variant?: 'success' | 'error' | 'warning' | 'info' | 'neutral';
}

/**
 * StatusBadge Component
 * 
 * A reusable status badge component that displays status with color-coded badges.
 * 
 * Features:
 * - Maps status values to DaisyUI badge colors (success, error, warning, info, neutral)
 * - Uses rounded-full border radius for pill-shaped badges
 * - Automatically determines variant based on common status keywords if not provided
 * - Uses Design_System typography (DM Sans for body text)
 * - Fully accessible with proper text contrast
 * 
 * Requirements satisfied:
 * - 16.5: Provide StatusBadge reusable component with color mapping
 * - 16.12: Pure presentation component without business logic
 * 
 * @example
 * ```tsx
 * <StatusBadge status="active" variant="success" />
 * <StatusBadge status="pending" variant="warning" />
 * <StatusBadge status="error" variant="error" />
 * <StatusBadge status="inactive" variant="neutral" />
 * ```
 */
export function StatusBadge({ status, variant }: StatusBadgeProps) {
  // Auto-determine variant based on status keywords if not provided
  const badgeVariant = variant || getVariantFromStatus(status);
  
  return (
    <span
      className={`badge badge-${badgeVariant} rounded-full text-xs font-medium px-3 py-2`}
      role="status"
      aria-label={`Status: ${status}`}
    >
      {status}
    </span>
  );
}

/**
 * Helper function to determine badge variant from status string
 * Maps common status keywords to appropriate badge colors
 */
function getVariantFromStatus(status: string): 'success' | 'error' | 'warning' | 'info' | 'neutral' {
  const lowerStatus = status.toLowerCase();
  
  // Success states
  if (lowerStatus.includes('active') || 
      lowerStatus.includes('success') || 
      lowerStatus.includes('complete') ||
      lowerStatus.includes('approved') ||
      lowerStatus.includes('available')) {
    return 'success';
  }
  
  // Error states
  if (lowerStatus.includes('error') || 
      lowerStatus.includes('failed') || 
      lowerStatus.includes('rejected') ||
      lowerStatus.includes('unavailable')) {
    return 'error';
  }
  
  // Warning states
  if (lowerStatus.includes('warning') || 
      lowerStatus.includes('pending') || 
      lowerStatus.includes('processing') ||
      lowerStatus.includes('in progress')) {
    return 'warning';
  }
  
  // Info states
  if (lowerStatus.includes('info') || 
      lowerStatus.includes('draft') || 
      lowerStatus.includes('new')) {
    return 'info';
  }
  
  // Default to neutral
  return 'neutral';
}
