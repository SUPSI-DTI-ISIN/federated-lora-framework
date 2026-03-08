# ThemeToggle Component

## Overview

The `ThemeToggle` component is a reusable UI component that manages dark/light theme switching with localStorage persistence. It's integrated into the application's header and provides a seamless theme switching experience.

## Features

- **localStorage Persistence**: Theme preference is saved to localStorage under the key "theme"
- **OS Preference Detection**: Automatically detects system theme preference when no saved theme exists
- **DaisyUI Integration**: Updates the `data-theme` attribute on the `<html>` element for DaisyUI theme switching
- **Animated Transitions**: Uses Framer Motion AnimatePresence for smooth icon transitions
- **Accessible**: Includes proper aria-label and title attributes for screen readers
- **Internationalized**: Uses react-i18next for translated labels

## Usage

```tsx
import { ThemeToggle } from './components/common/ThemeToggle';

// Basic usage
<ThemeToggle />

// With custom className
<ThemeToggle className="ml-4" />
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `className` | `string` | `''` | Optional CSS classes to apply to the button |

## Implementation Details

### Theme Detection Priority

1. **localStorage**: Checks for saved theme preference first
2. **OS Preference**: Falls back to `window.matchMedia('(prefers-color-scheme: dark)')` if no saved preference
3. **Default**: Uses detected theme and saves it to localStorage

### Theme Switching

When the user clicks the toggle button:
1. Theme state is updated (light ↔ dark)
2. `data-theme` attribute is set on `document.documentElement`
3. New theme is saved to localStorage

### Icons

- **Light Mode**: Displays Moon icon (clicking switches to dark mode)
- **Dark Mode**: Displays Sun icon (clicking switches to light mode)

### Animation

The icon transition uses Framer Motion with:
- Scale animation: 0.8 → 1
- Rotation: -90° → 0° (entrance) / 0° → 90° (exit)
- Opacity: 0 → 1
- Duration: 0.2s

## Integration

The ThemeToggle is integrated into the Header component:
- Desktop: Appears in the navbar-end section, before the profile menu
- Mobile: Appears in the mobile menu under the "Theme" section

## Translation Keys

The component uses the following translation keys:

```json
{
  "theme": {
    "light": "Switch to light mode",
    "dark": "Switch to dark mode"
  },
  "header": {
    "settings": {
      "theme": "Theme"
    }
  }
}
```

## Requirements Satisfied

This component satisfies the following requirements from the spec:

- **2.1**: Persist theme preference in localStorage under the key "theme"
- **2.2**: Detect OS preference using window.matchMedia when no saved preference exists
- **2.3**: Apply saved theme on application initialization
- **2.4**: Update data-theme attribute on the html element when theme changes
- **2.5**: Save new preference to localStorage when theme is toggled
- **2.6**: Provide toggle component with Sun icon for light mode and Moon icon for dark mode
- **2.7**: Place toggle in the top navbar right side
- **2.8**: Animate icon transition using Framer Motion AnimatePresence

## Browser Compatibility

- Requires localStorage support
- Requires matchMedia API for OS preference detection
- Works with all modern browsers (Chrome, Firefox, Safari, Edge)
