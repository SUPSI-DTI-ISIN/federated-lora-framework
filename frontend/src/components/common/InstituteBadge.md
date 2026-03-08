# InstituteBadge Component

A reusable badge component that displays the institute name in the navbar with theme-specific indigo styling.

## Features

- Displays institute name with Building2 icon prefix (14px size)
- Uses theme-specific indigo colors:
  - Light theme: border-indigo-200, bg-indigo-50, text-indigo-700
  - Dark theme: border-indigo-700, bg-indigo-950, text-indigo-300
- Truncates long names (>20 characters) with ellipsis
- Shows full name in tooltip on hover when truncated
- Uses Design_System typography (DM Sans medium font at text-sm size)
- Fully accessible with proper ARIA labels
- Display-only component (not clickable)

## Props

```typescript
interface InstituteBadgeProps {
  instituteName: string;  // The institute name to display
  className?: string;     // Optional additional CSS classes
}
```

## Usage

### Basic Usage

```tsx
import { InstituteBadge } from '@/components/common';

// Short name - displays fully
<InstituteBadge instituteName="MIT" />

// Medium name - displays fully
<InstituteBadge instituteName="University of Tech" />

// Long name - truncates with tooltip
<InstituteBadge instituteName="Massachusetts Institute of Technology" />
```

### With Realm Context

```tsx
import { InstituteBadge } from '@/components/common';
import { useSelectorRealm } from '@/hooks/realm/useSelectorRealm';

function Navbar() {
  const { realm } = useSelectorRealm();
  
  return (
    <nav>
      {/* Other navbar elements */}
      {realm && <InstituteBadge instituteName={realm} />}
    </nav>
  );
}
```

### With Custom Styling

```tsx
// Add additional spacing or positioning
<InstituteBadge 
  instituteName="University Name" 
  className="ml-4" 
/>
```

## Truncation Behavior

- Names with 20 or fewer characters: Display fully without truncation
- Names with more than 20 characters: 
  - Display first 20 characters followed by "..."
  - Show full name in DaisyUI tooltip on hover
  - Tooltip appears below the badge (tooltip-bottom)

## Design System

- **Border Radius**: `rounded-full` (pill shape)
- **Typography**: DM Sans font, text-sm size, font-medium weight
- **Icon**: Building2 from Lucide React, 14px size, strokeWidth 2
- **Spacing**: px-3 py-1.5 padding, gap-2 between icon and text
- **Colors**: 
  - Light: border-indigo-200, bg-indigo-50, text-indigo-700
  - Dark: border-indigo-700, bg-indigo-950, text-indigo-300

## Accessibility

- Uses semantic `role="status"` attribute
- Includes `aria-label` with full institute name
- Icon has `aria-hidden="true"` to prevent screen reader duplication
- Tooltip provides full text for truncated names
- Not interactive (no focus or click handlers needed)

## Requirements Satisfied

- **5.1**: Read INSTITUTE_NAME from realm context (via props)
- **5.2**: Display between app logo and navbar spacer
- **5.3**: Render as pill/badge with indigo border and text
- **5.4**: Light theme colors (border-indigo-200 bg-indigo-50 text-indigo-700)
- **5.5**: Dark theme colors (border-indigo-700 bg-indigo-950 text-indigo-300)
- **5.6**: Use DM Sans medium font at text-sm size
- **5.7**: Display Building2 icon prefix at 14px size
- **5.8**: Truncate long names with ellipsis and tooltip
- **5.9**: Visible on all pages (when integrated into navbar)
- **5.10**: Not clickable
- **16.7**: Provide InstituteBadge reusable component
- **16.14**: Only display data passed via props

## Integration Notes

This component should be integrated into the navbar between the app logo and the main navigation spacer. It receives the institute name as a prop, typically from the `useSelectorRealm()` hook.

The component is purely presentational and contains no business logic - it only displays the data passed to it via props.
