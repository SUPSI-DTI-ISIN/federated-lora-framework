# EmptyState Component

A reusable empty state component that displays when no data is available.

## Features

- Displays icon with title and optional description
- Supports optional action button with label and onClick handler
- Uses centered layout with generous whitespace
- Uses Design_System typography (Plus Jakarta Sans for headings, DM Sans for body)
- Uses Design_System spacing and colors
- Fully responsive layout

## Requirements Satisfied

- **16.3**: Provide EmptyState reusable component
- **16.10**: Pure presentation component without business logic

## Props

```typescript
interface EmptyStateProps {
  icon: LucideIcon;           // Icon component from lucide-react
  title: string;              // Main title text
  description?: string;       // Optional description text
  action?: {                  // Optional action button
    label: string;            // Button label
    onClick: () => void;      // Button click handler
  };
}
```

## Usage Examples

### Basic Empty State (No Action)

```tsx
import { MessageSquare } from 'lucide-react';
import { EmptyState } from '@/components/common';

function ChatsPage() {
  return (
    <EmptyState
      icon={MessageSquare}
      title="No chats yet"
      description="Start a new conversation to get started"
    />
  );
}
```

### Empty State with Action Button

```tsx
import { FileText } from 'lucide-react';
import { EmptyState } from '@/components/common';

function DocumentsPage() {
  const handleUpload = () => {
    // Handle upload action
  };

  return (
    <EmptyState
      icon={FileText}
      title="No documents"
      description="Upload your first PDF document to get started"
      action={{
        label: "Upload Document",
        onClick: handleUpload
      }}
    />
  );
}
```

### Empty State without Description

```tsx
import { Plug } from 'lucide-react';
import { EmptyState } from '@/components/common';

function AdaptersPage() {
  const handleCreate = () => {
    // Handle create action
  };

  return (
    <EmptyState
      icon={Plug}
      title="No adapters configured"
      action={{
        label: "Create Adapter",
        onClick: handleCreate
      }}
    />
  );
}
```

## Styling

The component uses:
- **Icon**: 48px size with light stroke (1.5), displayed in a circular background
- **Title**: text-xl font-semibold
- **Description**: text-base with 60% opacity
- **Action Button**: DaisyUI btn btn-primary styling
- **Layout**: Centered with generous whitespace (min-h-[400px], p-8)
- **Max Width**: max-w-md for optimal readability

## Accessibility

- Icon has `aria-hidden="true"` as it's decorative
- Button has proper type="button" attribute
- Text hierarchy is semantic (h3 for title, p for description)

## Design System Compliance

- Uses DaisyUI theme colors (base-content, base-200)
- Uses consistent spacing (mb-6, mb-2, p-6, p-8)
- Uses rounded-full for icon background
- Fully responsive and works across all viewport sizes
