# PageHeader Component

A reusable page header component that provides consistent page headers across all pages.

## Features

- Displays optional icon with title
- Shows optional subtitle text
- Supports optional action button with icon and onClick handler
- Uses Design_System typography (Plus Jakarta Sans for headings, DM Sans for body)
- Uses Design_System spacing (p-6 for sections, gap-4 for elements)
- Fully responsive layout (stacks vertically on mobile, horizontal on desktop)

## Props

```typescript
interface PageHeaderProps {
  icon?: LucideIcon;           // Optional icon from Lucide React
  title: string;               // Page title (required)
  subtitle?: string;           // Optional subtitle text
  action?: {                   // Optional action button
    label: string;             // Button label
    icon?: LucideIcon;         // Optional button icon
    onClick: () => void;       // Click handler
  };
}
```

## Usage Examples

### Basic Header (Title Only)

```tsx
import { PageHeader } from '@/components/common';

<PageHeader title="Settings" />
```

### Header with Icon and Subtitle

```tsx
import { PageHeader } from '@/components/common';
import { FileText } from 'lucide-react';

<PageHeader
  icon={FileText}
  title="Documents"
  subtitle="Manage your PDF documents"
/>
```

### Header with Action Button

```tsx
import { PageHeader } from '@/components/common';
import { MessageSquare, MessageSquarePlus } from 'lucide-react';

<PageHeader
  icon={MessageSquare}
  title="Chats"
  subtitle="Your conversation history"
  action={{
    label: "New Chat",
    icon: MessageSquarePlus,
    onClick: handleNewChat
  }}
/>
```

### Header with All Props

```tsx
import { PageHeader } from '@/components/common';
import { FileText, Upload } from 'lucide-react';

<PageHeader
  icon={FileText}
  title="Documents"
  subtitle="Upload and manage your PDF files"
  action={{
    label: "Upload Document",
    icon: Upload,
    onClick: handleUpload
  }}
/>
```

## Styling

The component uses:
- **Typography**: 
  - Title: `text-3xl font-bold` (Plus Jakarta Sans via Design_System)
  - Subtitle: `text-base` (DM Sans via Design_System)
- **Spacing**: 
  - Bottom margin: `mb-6`
  - Internal gap: `gap-4` (between elements), `gap-3` (icon and text)
- **Colors**: 
  - Icon: `text-primary` (theme-aware)
  - Title: `text-base-content` (theme-aware)
  - Subtitle: `text-base-content/70` (70% opacity)
- **Responsive**: 
  - Mobile: Stacks vertically (`flex-col`)
  - Desktop: Horizontal layout (`sm:flex-row sm:items-center sm:justify-between`)

## Accessibility

- Icon has `aria-hidden="true"` (decorative)
- Button has proper `type="button"` attribute
- Semantic HTML structure with proper heading hierarchy

## Requirements Satisfied

- **16.2**: Provide PageHeader reusable component accepting title, subtitle, and optional CTA button props
- **16.9**: Pure presentation component without business logic

## Design System Compliance

- Uses DaisyUI button component (`btn btn-primary`)
- Uses theme-aware colors (`text-base-content`, `text-primary`)
- Uses consistent icon sizing (32px for page icon, 16px for button icon)
- Uses consistent spacing from Design_System
- Fully responsive across all viewport sizes
