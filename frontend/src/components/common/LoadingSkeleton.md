# LoadingSkeleton Component

A reusable loading skeleton component that displays loading states matching the layout structure of loaded content.

## Features

- Supports variants for list, card, and table layouts
- Uses DaisyUI skeleton component with theme-appropriate colors
- Configurable count of skeleton items to display
- Matches the structure of actual content for smooth transitions
- Uses Design_System colors and spacing
- Includes proper ARIA attributes for accessibility

## Props

```typescript
interface LoadingSkeletonProps {
  variant: 'list' | 'card' | 'table';
  count?: number;
}
```

### variant (required)
- Type: `'list' | 'card' | 'table'`
- Description: The layout variant to render
  - `'list'`: Displays skeleton items in a vertical list layout with icon, content, and action areas
  - `'card'`: Displays skeleton items in a responsive card grid layout
  - `'table'`: Displays skeleton items in a table layout with headers and rows

### count (optional)
- Type: `number`
- Default: `3`
- Description: Number of skeleton items to display

## Usage Examples

### List Variant
```tsx
import { LoadingSkeleton } from '@/components/common';

function DocumentsPage() {
  const { data, isLoading } = useDocuments();

  if (isLoading) {
    return <LoadingSkeleton variant="list" count={5} />;
  }

  return <DocumentList documents={data} />;
}
```

### Card Variant
```tsx
import { LoadingSkeleton } from '@/components/common';

function AdaptersPage() {
  const { data, isLoading } = useAdapters();

  if (isLoading) {
    return <LoadingSkeleton variant="card" count={6} />;
  }

  return <AdapterGrid adapters={data} />;
}
```

### Table Variant
```tsx
import { LoadingSkeleton } from '@/components/common';

function UsersPage() {
  const { data, isLoading } = useUsers();

  if (isLoading) {
    return <LoadingSkeleton variant="table" count={10} />;
  }

  return <UserTable users={data} />;
}
```

## Accessibility

- Uses `role="status"` to indicate loading state to screen readers
- Includes `aria-label="Loading content"` for context
- Provides `sr-only` text "Loading..." for screen reader users
- Respects theme colors for proper contrast

## Requirements Satisfied

- **16.4**: Provide LoadingSkeleton reusable component
- **16.11**: Pure presentation component without business logic
- **17.1**: Render Loading_State using DaisyUI skeleton loaders
- **17.2**: Match layout structure of loaded content
- **17.7**: Use Design_System colors and spacing

## Design System Integration

The component uses:
- DaisyUI base colors (`base-100`, `base-300`)
- Tailwind CSS utility classes for layout and spacing
- `animate-pulse` for loading animation
- Consistent border radius (`rounded-lg`, `rounded-full`)
- Design system spacing (`gap-4`, `p-4`, `p-6`)
