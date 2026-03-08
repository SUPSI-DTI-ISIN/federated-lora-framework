# StatusBadge Component

A reusable status badge component that displays status with color-coded badges using DaisyUI styling.

## Features

- Maps status values to DaisyUI badge colors (success, error, warning, info, neutral)
- Uses rounded-full border radius for pill-shaped badges
- Automatically determines variant based on common status keywords if not provided
- Uses Design_System typography (DM Sans for body text)
- Fully accessible with proper text contrast and ARIA labels

## Props

```typescript
interface StatusBadgeProps {
  status: string;           // The status text to display
  variant?: 'success' | 'error' | 'warning' | 'info' | 'neutral';  // Optional badge color variant
}
```

## Usage

### Basic Usage with Auto-Detection

```tsx
import { StatusBadge } from '@/components/common';

// Auto-detects variant based on status text
<StatusBadge status="active" />        // → success (green)
<StatusBadge status="pending" />       // → warning (yellow)
<StatusBadge status="error" />         // → error (red)
<StatusBadge status="inactive" />      // → neutral (gray)
<StatusBadge status="processing" />    // → warning (yellow)
```

### Explicit Variant

```tsx
// Explicitly set the variant
<StatusBadge status="Custom Status" variant="success" />
<StatusBadge status="In Review" variant="info" />
<StatusBadge status="Blocked" variant="error" />
```

## Auto-Detection Rules

The component automatically determines the badge color based on status keywords:

- **Success (green)**: active, success, complete, approved, available
- **Error (red)**: error, failed, rejected, unavailable
- **Warning (yellow)**: warning, pending, processing, in progress
- **Info (blue)**: info, draft, new
- **Neutral (gray)**: default for unmatched statuses

## Design System

- **Border Radius**: `rounded-full` (pill shape)
- **Typography**: DM Sans font, text-xs size, font-medium weight
- **Spacing**: px-3 py-2 padding
- **Colors**: DaisyUI badge variants (badge-success, badge-error, badge-warning, badge-info, badge-neutral)

## Accessibility

- Uses semantic `role="status"` attribute
- Includes `aria-label` with full status text
- Ensures WCAG AA contrast compliance through DaisyUI badge colors

## Requirements Satisfied

- **16.5**: Provide StatusBadge reusable component with color mapping
- **16.12**: Pure presentation component without business logic
