# NavigationShell Component

## Overview

The `NavigationShell` is a top-level layout wrapper that provides consistent navigation structure across all pages of the application. It implements a responsive layout with a top navbar, collapsible sidebar, and main content area.

## Features

- **Top Navbar**: Sticky h-16 navbar at the top (provided by Header component)
- **Responsive Sidebar**:
  - Desktop (≥1280px): Full sidebar with icons and labels (w-64)
  - Tablet (≥768px and <1280px): Collapsed icon-only sidebar (w-16) with tooltips
  - Mobile (<768px): Hidden sidebar with drawer overlay
- **Main Content Area**: Centered container with max-w-screen-2xl
- **Responsive Padding**: p-6 on desktop, p-4 on mobile
- **Smooth Animations**: Framer Motion transitions for drawer and sidebar
- **Accessibility**: Full keyboard navigation, ARIA labels, and Escape key support

## Usage

```tsx
import { NavigationShell } from "@/components/layout";

function App() {
  return (
    <NavigationShell>
      <YourPageContent />
    </NavigationShell>
  );
}
```

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `children` | `React.ReactNode` | Yes | The page content to render inside the shell |

## Responsive Behavior

### Desktop (≥1280px)
- Full sidebar visible with icons and labels
- Width: w-64 (256px)
- Navigation items show icon + text
- Active route highlighted with indigo left border and background tint

### Tablet (≥768px and <1280px)
- Collapsed sidebar with icons only
- Width: w-16 (64px)
- Tooltips appear on hover to show labels
- Active route highlighted with background tint

### Mobile (<768px)
- Sidebar hidden by default
- Drawer overlay triggered by hamburger menu in navbar
- Drawer slides in from left with backdrop
- Background scroll prevented when drawer is open
- Closes on route change, Escape key, or backdrop click

## Navigation Links

The component automatically determines which navigation links to display based on:
- Authentication state (public vs protected routes)
- User role (regular user vs department admin)

Links are defined with:
- Path (route)
- Label key (for i18n translation)
- Icon (from Lucide React)

## Accessibility

- Semantic HTML (`<nav>`, `<aside>`, `<main>`)
- ARIA labels for navigation regions
- Keyboard navigation support
- Escape key closes drawer
- Focus indicators for keyboard users
- Minimum 44x44px touch targets on mobile

## Requirements Satisfied

- 3.1: Top navbar with h-16 sticky positioning
- 3.2: Sidebar on left with w-64 on desktop
- 3.3: Main content area to the right of sidebar
- 3.4: Display sidebar with icons and labels on desktop (≥1280px)
- 3.5: Collapse sidebar to icon-only (w-16) on tablet (≥768px and <1280px)
- 3.6: Hide sidebar and provide drawer overlay on mobile (<768px)
- 3.8: Contain main content within max-w-screen-2xl mx-auto container
- 3.9: Apply p-6 padding on desktop, p-4 on mobile
- 9.5-9.9: Responsive layout requirements

## Related Components

- `Header`: Top navbar component with logo, theme toggle, language switcher, and user menu
- `InstituteBadge`: Institute name badge displayed in navbar
- `ThemeToggle`: Dark/light theme toggle button

## Notes

- The component preserves all existing business logic and routing
- Navigation links are automatically filtered based on authentication state
- Drawer state is managed internally and resets on route changes
- Background scroll is prevented when drawer is open on mobile
