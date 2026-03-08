# Requirements Document

## Introduction

This document specifies the requirements for a complete UI/UX visual refactor of the existing React + TypeScript frontend application. The refactor focuses exclusively on graphical components and styles while preserving all business logic, API calls, data-fetching hooks, routing logic, state management, service clients, authentication flows, and component file structure.

The goal is to transform the interface into a world-class, modern SaaS enterprise interface — clean, formal, elegant, and immediately intuitive — using only the libraries already present in the project's package.json.

## Glossary

- **UI_System**: The complete user interface layer including all visual components, styles, and animations
- **Design_System**: The cohesive set of design tokens, color palettes, typography, spacing, and component patterns
- **Theme_Manager**: The system responsible for managing and persisting dark/light theme preferences
- **Navigation_Shell**: The application's top-level layout structure including navbar, sidebar, and main content area
- **Delete_Modal**: A confirmation dialog that appears before any destructive action
- **Translation_System**: The i18n system using react-i18next for multilingual support
- **Institute_Badge**: A visual component displaying the INSTITUTE_NAME in the navbar
- **Responsive_Layout**: Layout system that adapts to mobile (≥320px), tablet (≥768px), desktop (≥1280px), and wide (≥1920px) viewports
- **Motion_System**: Animation framework using Framer Motion for transitions and micro-interactions
- **Toast_Notification**: Temporary notification messages displayed via React Hot Toast
- **Page_Component**: Any top-level route component (Home, Documents, Chat, Adapters, etc.)
- **Reusable_Component**: Pure UI components used across multiple pages
- **Loading_State**: Visual feedback shown while data is being fetched
- **Empty_State**: Visual feedback shown when no data is available
- **Error_State**: Visual feedback shown when an error occurs

## Requirements

### Requirement 1: Design System Implementation

**User Story:** As a developer, I want a cohesive design system implemented using Tailwind CSS v4 and DaisyUI v5, so that the interface has consistent visual language throughout.

#### Acceptance Criteria

1. THE Design_System SHALL use Tailwind CSS v4 utility classes for all styling
2. THE Design_System SHALL use DaisyUI v5 components as the base component layer
3. THE Design_System SHALL define a light theme with background #F8F9FB, primary #4F46E5, and surface #FFFFFF
4. THE Design_System SHALL define a dark theme with background #0F1117, primary #6366F1, and surface #1A1D27
5. THE Design_System SHALL use Plus Jakarta Sans font (weights 600, 700) for headings
6. THE Design_System SHALL use DM Sans font (weights 400, 500) for body text
7. THE Design_System SHALL use JetBrains Mono font (weight 400) for monospace content
8. THE Design_System SHALL use border-radius values of rounded-xl for cards, rounded-lg for buttons and inputs, and rounded-full for badges
9. THE Design_System SHALL use consistent padding of p-6 for cards and p-4 for compact panels
10. FOR ALL color values, THE Design_System SHALL ensure WCAG AA contrast compliance between text and backgrounds

### Requirement 2: Theme Management

**User Story:** As a user, I want to toggle between dark and light themes, so that I can use the interface in my preferred visual mode.

#### Acceptance Criteria

1. THE Theme_Manager SHALL persist theme preference in localStorage under the key "theme"
2. WHEN the application initializes AND no saved preference exists, THE Theme_Manager SHALL detect the OS preference using window.matchMedia('(prefers-color-scheme: dark)')
3. WHEN the application initializes AND a saved preference exists, THE Theme_Manager SHALL apply the saved theme
4. WHEN a user toggles the theme, THE Theme_Manager SHALL update the data-theme attribute on the html element
5. WHEN a user toggles the theme, THE Theme_Manager SHALL save the new preference to localStorage
6. THE Theme_Manager SHALL provide a toggle component with Sun icon for light mode and Moon icon for dark mode
7. THE Theme_Manager SHALL place the toggle in the top navbar right side
8. WHEN the theme changes, THE Theme_Manager SHALL animate the icon transition using Framer Motion AnimatePresence

### Requirement 3: Navigation Shell Layout

**User Story:** As a user, I want a consistent navigation structure across all pages, so that I can easily navigate the application.

#### Acceptance Criteria

1. THE Navigation_Shell SHALL render a top navbar with height h-16 that remains sticky at the top
2. THE Navigation_Shell SHALL render a sidebar on the left side with width w-64 on desktop
3. THE Navigation_Shell SHALL render a main content area to the right of the sidebar
4. WHEN viewport width is ≥1280px, THE Navigation_Shell SHALL display the sidebar with icons and labels
5. WHEN viewport width is ≥768px AND <1280px, THE Navigation_Shell SHALL collapse the sidebar to icon-only mode with width w-16
6. WHEN viewport width is <768px, THE Navigation_Shell SHALL hide the sidebar and provide a drawer overlay toggle
7. THE Navigation_Shell SHALL animate sidebar collapse transitions with duration 0.3s and easeInOut easing
8. THE Navigation_Shell SHALL contain the main content within a max-w-screen-2xl mx-auto container
9. THE Navigation_Shell SHALL apply p-6 padding to main content on desktop and p-4 on mobile

### Requirement 4: Top Navbar Components

**User Story:** As a user, I want a functional top navbar with all essential controls, so that I can access key features and settings.

#### Acceptance Criteria

1. THE Navigation_Shell SHALL render a hamburger/collapse icon as the leftmost navbar element
2. THE Navigation_Shell SHALL render the app logo and app name after the hamburger icon
3. THE Navigation_Shell SHALL render the Institute_Badge after the app logo
4. THE Navigation_Shell SHALL render a language switcher in the right section of the navbar
5. THE Navigation_Shell SHALL render the theme toggle after the language switcher
6. THE Navigation_Shell SHALL render a user avatar/profile menu as the rightmost navbar element
7. WHEN the hamburger icon is clicked on mobile, THE Navigation_Shell SHALL toggle the sidebar drawer
8. WHEN the hamburger icon is clicked on desktop, THE Navigation_Shell SHALL toggle sidebar collapse state
9. WHEN the user avatar is clicked, THE Navigation_Shell SHALL display a dropdown with user info and logout option
10. THE Navigation_Shell SHALL wire the logout option to the existing OIDC logout function

### Requirement 5: Institute Name Display

**User Story:** As a user, I want to see the institute name prominently displayed, so that I know which organization's system I'm using.

#### Acceptance Criteria

1. THE Institute_Badge SHALL read INSTITUTE_NAME from the existing realm context
2. THE Institute_Badge SHALL display between the app logo and the navbar spacer
3. THE Institute_Badge SHALL render as a pill/badge with indigo border and indigo text
4. WHEN light theme is active, THE Institute_Badge SHALL use border-indigo-200 bg-indigo-50 text-indigo-700
5. WHEN dark theme is active, THE Institute_Badge SHALL use border-indigo-700 bg-indigo-950 text-indigo-300
6. THE Institute_Badge SHALL use DM Sans medium font at text-sm size
7. THE Institute_Badge SHALL display a Building2 icon prefix at 14px size
8. WHEN INSTITUTE_NAME length exceeds 20 characters, THE Institute_Badge SHALL truncate with ellipsis and show full name in tooltip
9. THE Institute_Badge SHALL be visible on all pages
10. THE Institute_Badge SHALL NOT be clickable

### Requirement 6: Sidebar Navigation

**User Story:** As a user, I want a sidebar with clear navigation links, so that I can quickly access different sections of the application.

#### Acceptance Criteria

1. THE Navigation_Shell SHALL render navigation items with icons from Lucide React
2. THE Navigation_Shell SHALL render navigation labels using the Translation_System
3. WHEN a route is active, THE Navigation_Shell SHALL highlight the nav item with indigo left-border accent and subtle background tint
4. THE Navigation_Shell SHALL map nav items to existing routes without adding or removing routes
5. WHEN sidebar is collapsed, THE Navigation_Shell SHALL show icon-only nav items with tooltips
6. WHEN sidebar is expanded, THE Navigation_Shell SHALL show icon + label nav items
7. THE Navigation_Shell SHALL render an app version or branding element in the sidebar footer
8. WHEN viewport is mobile, THE Navigation_Shell SHALL render sidebar as a drawer overlay
9. WHEN drawer overlay is open, THE Navigation_Shell SHALL prevent background scroll
10. WHEN drawer overlay background is clicked OR Escape key is pressed, THE Navigation_Shell SHALL close the drawer

### Requirement 7: Delete Confirmation Modal

**User Story:** As a user, I want to confirm destructive actions before they execute, so that I don't accidentally delete important data.

#### Acceptance Criteria

1. WHEN any delete action is triggered, THE Delete_Modal SHALL display before executing the deletion
2. THE Delete_Modal SHALL use DaisyUI modal component as the base
3. THE Delete_Modal SHALL render a dark overlay with bg-black/60 backdrop-blur-sm
4. WHEN the modal is open, THE Delete_Modal SHALL freeze the background page by preventing scroll and interaction
5. THE Delete_Modal SHALL display an AlertTriangle icon from Lucide in error/red color
6. THE Delete_Modal SHALL display a translated title using t('modal.delete.title')
7. THE Delete_Modal SHALL display a translated message using t('modal.delete.message')
8. WHEN an itemName is provided, THE Delete_Modal SHALL display a translated message using t('modal.delete.messageNamed') with the item name
9. THE Delete_Modal SHALL render a Cancel button using btn btn-ghost styling that closes the modal without action
10. THE Delete_Modal SHALL render a Delete button using btn btn-error styling that executes the provided onConfirm callback
11. THE Delete_Modal SHALL animate entrance using Framer Motion with scale 0.95→1 and opacity 0→1 over 0.2s
12. WHEN overlay is clicked, THE Delete_Modal SHALL close without executing deletion
13. WHEN Escape key is pressed, THE Delete_Modal SHALL close without executing deletion
14. THE Delete_Modal SHALL accept isOpen, onConfirm, onCancel, and optional itemName props

### Requirement 8: Internationalization

**User Story:** As a user, I want all UI text to be translatable, so that I can use the application in my preferred language.

#### Acceptance Criteria

1. THE Translation_System SHALL use react-i18next for all UI text
2. THE UI_System SHALL NOT render any hardcoded strings in JSX
3. THE Translation_System SHALL call the t() function for every UI text string
4. THE Translation_System SHALL support English (en) and Italian (it) locales
5. THE Translation_System SHALL store translations in src/i18n/locales/en/translations.json
6. THE Translation_System SHALL store translations in src/i18n/locales/it/translations.json
7. THE Translation_System SHALL include translation keys for common actions: loading, error, retry, cancel, save, delete, edit, view, upload
8. THE Translation_System SHALL include translation keys for modal.delete: title, message, messageNamed, confirm, cancel
9. THE Translation_System SHALL include translation keys for navigation: home, documents, chats, adapters, settings, logout
10. THE Translation_System SHALL include translation keys for theme toggle: light, dark
11. THE Translation_System SHALL include translation keys for all page-specific content
12. THE Translation_System SHALL preserve all existing translation keys

### Requirement 9: Responsive Layout

**User Story:** As a user, I want the interface to work well on all device sizes, so that I can use it on mobile, tablet, and desktop.

#### Acceptance Criteria

1. THE Responsive_Layout SHALL support mobile viewports with minimum width 320px
2. THE Responsive_Layout SHALL support tablet viewports with minimum width 768px
3. THE Responsive_Layout SHALL support desktop viewports with minimum width 1280px
4. THE Responsive_Layout SHALL support wide viewports with minimum width 1920px
5. WHEN viewport is <768px, THE Responsive_Layout SHALL hide the sidebar and use drawer navigation
6. WHEN viewport is ≥768px AND <1280px, THE Responsive_Layout SHALL collapse sidebar to icon-only mode
7. WHEN viewport is ≥1280px, THE Responsive_Layout SHALL display full sidebar with icons and labels
8. WHEN viewport is <768px, THE Responsive_Layout SHALL use p-4 padding for main content
9. WHEN viewport is ≥768px, THE Responsive_Layout SHALL use p-6 padding for main content
10. THE Responsive_Layout SHALL ensure all interactive elements have minimum touch target size of 44x44px on mobile

### Requirement 10: Animation System

**User Story:** As a user, I want smooth, polished animations, so that the interface feels responsive and professional.

#### Acceptance Criteria

1. THE Motion_System SHALL use Framer Motion v12 for all animations
2. WHEN a page loads, THE Motion_System SHALL animate entrance with fade and upward slide (y: 12→0, opacity: 0→1, duration: 0.25s)
3. WHEN a modal opens, THE Motion_System SHALL animate entrance with scale and fade (scale: 0.95→1, opacity: 0→1, duration: 0.2s)
4. WHEN list items render, THE Motion_System SHALL stagger fade-in with staggerChildren: 0.05s
5. WHEN a card is hovered, THE Motion_System SHALL apply subtle lift (y: -2px) and increase shadow
6. WHEN sidebar collapses or expands, THE Motion_System SHALL animate width transition with duration 0.3s and easeInOut easing
7. THE Motion_System SHALL respect prefers-reduced-motion media query
8. WHEN prefers-reduced-motion is set, THE Motion_System SHALL disable or reduce all animations
9. THE Motion_System SHALL wrap each Page_Component in a motion.div for entrance animation
10. THE Motion_System SHALL use AnimatePresence for modal and dropdown transitions

### Requirement 11: Toast Notifications

**User Story:** As a user, I want consistent notification styling, so that success and error messages are clear and match the design system.

#### Acceptance Criteria

1. THE Toast_Notification SHALL use React Hot Toast for all notifications
2. THE Toast_Notification SHALL position toasts at bottom-right
3. THE Toast_Notification SHALL display toasts for 4000ms duration
4. WHEN light theme is active, THE Toast_Notification SHALL use light theme colors matching the Design_System
5. WHEN dark theme is active, THE Toast_Notification SHALL use dark theme colors matching the Design_System
6. THE Toast_Notification SHALL use DM Sans font matching the Design_System
7. THE Toast_Notification SHALL use rounded-lg border radius
8. THE Toast_Notification SHALL include appropriate icons for success, error, and info states
9. THE Toast_Notification SHALL use translated text via the Translation_System
10. THE Toast_Notification SHALL NOT modify existing toast trigger logic

### Requirement 12: Home Page Visual Refactor

**User Story:** As a user, I want an elegant home page, so that I have a welcoming entry point to the application.

#### Acceptance Criteria

1. THE Home Page_Component SHALL render a welcome hero section with greeting using t('home.welcome') and user name
2. WHEN user data is available, THE Home Page_Component SHALL display summary stat cards using DaisyUI stats component
3. WHEN no user data is available, THE Home Page_Component SHALL render an empty state with app logo, t('home.tagline'), and t('home.description')
4. THE Home Page_Component SHALL use centered layout with generous whitespace
5. THE Home Page_Component SHALL apply indigo accent colors to stat cards
6. THE Home Page_Component SHALL animate entrance using the Motion_System
7. THE Home Page_Component SHALL be fully responsive across all viewport sizes
8. THE Home Page_Component SHALL NOT modify any existing data fetching hooks
9. THE Home Page_Component SHALL NOT modify any existing business logic
10. THE Home Page_Component SHALL preserve all existing props and state variables

### Requirement 13: Documents Page Visual Refactor

**User Story:** As a user, I want a polished documents page, so that I can easily upload and manage PDF files.

#### Acceptance Criteria

1. THE Documents Page_Component SHALL render a page header with t('documents.title'), t('documents.subtitle'), and upload button
2. THE Documents Page_Component SHALL render an upload button with Upload icon from Lucide and t('documents.upload') label
3. THE Documents Page_Component SHALL render a styled drag-and-drop zone with dashed indigo border and cloud upload icon
4. THE Documents Page_Component SHALL display translated hint text in the upload zone
5. THE Documents Page_Component SHALL render document list as a table or card grid matching existing data structure
6. WHEN documents exist, THE Documents Page_Component SHALL display columns for name, type badge, upload date, size, and actions
7. THE Documents Page_Component SHALL render a PDF badge in red/accent color for document type
8. THE Documents Page_Component SHALL render View and Delete action buttons as icon buttons
9. WHEN Delete button is clicked, THE Documents Page_Component SHALL trigger the Delete_Modal
10. WHEN no documents exist, THE Documents Page_Component SHALL render an empty state with t('documents.empty') and upload CTA
11. WHEN data is loading, THE Documents Page_Component SHALL render DaisyUI skeleton loaders
12. WHEN an error occurs, THE Documents Page_Component SHALL render a DaisyUI alert with error icon and t('documents.error')
13. THE Documents Page_Component SHALL NOT modify existing upload handler logic
14. THE Documents Page_Component SHALL NOT modify existing document fetching hooks
15. THE Documents Page_Component SHALL preserve all existing event handlers

### Requirement 14: Chat Page Visual Refactor

**User Story:** As a user, I want a clean chat interface, so that I can have productive conversations with the AI.

#### Acceptance Criteria

1. THE Chat Page_Component SHALL render a page header with t('chats.title'), t('chats.subtitle'), and New Chat button
2. THE Chat Page_Component SHALL render a New Chat button with MessageSquarePlus icon from Lucide
3. THE Chat Page_Component SHALL render chat list as card-based layout
4. WHEN chats exist, THE Chat Page_Component SHALL display each chat card with title or first message preview (truncated), timestamp, and right-arrow indicator
5. WHEN a chat card is hovered, THE Chat Page_Component SHALL apply subtle lift animation using Motion_System
6. WHEN a chat card is clicked, THE Chat Page_Component SHALL navigate to existing chat detail route
7. THE Chat Page_Component SHALL render a Trash2 icon button on each card for deletion
8. WHEN Delete button is clicked, THE Chat Page_Component SHALL trigger the Delete_Modal
9. WHEN no chats exist, THE Chat Page_Component SHALL render an empty state with MessageSquare icon, t('chats.empty'), and New Chat CTA
10. WHEN data is loading, THE Chat Page_Component SHALL render skeleton cards
11. THE Chat Page_Component SHALL NOT modify existing chat fetching hooks
12. THE Chat Page_Component SHALL NOT modify existing navigation logic
13. THE Chat Page_Component SHALL preserve all existing event handlers

### Requirement 15: Adapters Page Visual Refactor

**User Story:** As a user, I want a clear adapters page, so that I can manage model adapters effectively.

#### Acceptance Criteria

1. THE Adapters Page_Component SHALL render a page header with t('adapters.title') and t('adapters.subtitle')
2. THE Adapters Page_Component SHALL render adapters as a card grid layout
3. WHEN adapters exist, THE Adapters Page_Component SHALL display each card with adapter name (bold), status badge, type/category label, and action buttons
4. THE Adapters Page_Component SHALL render status badges using DaisyUI badge component
5. WHEN adapter status is active, THE Adapters Page_Component SHALL render a green badge
6. WHEN adapter status is inactive, THE Adapters Page_Component SHALL render a grey badge
7. THE Adapters Page_Component SHALL render Edit and Delete action buttons
8. WHEN Delete button is clicked, THE Adapters Page_Component SHALL trigger the Delete_Modal
9. WHEN no adapters exist, THE Adapters Page_Component SHALL render an empty state with Plug or Cpu icon from Lucide and t('adapters.empty')
10. WHEN data is loading, THE Adapters Page_Component SHALL render skeleton cards
11. THE Adapters Page_Component SHALL NOT modify existing adapter fetching hooks
12. THE Adapters Page_Component SHALL NOT modify existing action handlers
13. THE Adapters Page_Component SHALL preserve all existing props and state

### Requirement 16: Reusable UI Components

**User Story:** As a developer, I want reusable UI components, so that I can maintain consistency and reduce code duplication.

#### Acceptance Criteria

1. THE UI_System SHALL provide a DeleteConfirmModal Reusable_Component accepting isOpen, onConfirm, onCancel, and itemName props
2. THE UI_System SHALL provide a PageHeader Reusable_Component accepting title, subtitle, and optional CTA button props
3. THE UI_System SHALL provide an EmptyState Reusable_Component accepting icon, title, description, and optional CTA props
4. THE UI_System SHALL provide a LoadingSkeleton Reusable_Component matching list, card, and table layouts
5. THE UI_System SHALL provide a StatusBadge Reusable_Component with color mapping for status values
6. THE UI_System SHALL provide a ThemeToggle Reusable_Component for the navbar
7. THE UI_System SHALL provide an InstituteBadge Reusable_Component for the navbar
8. THE DeleteConfirmModal SHALL be pure presentation component without business logic
9. THE PageHeader SHALL be pure presentation component without business logic
10. THE EmptyState SHALL be pure presentation component without business logic
11. THE LoadingSkeleton SHALL be pure presentation component without business logic
12. THE StatusBadge SHALL be pure presentation component without business logic
13. THE ThemeToggle SHALL manage only theme state and localStorage persistence
14. THE InstituteBadge SHALL only display data passed via props

### Requirement 17: Loading and Error States

**User Story:** As a user, I want clear feedback when data is loading or errors occur, so that I understand the application state.

#### Acceptance Criteria

1. WHEN data is being fetched, THE Page_Component SHALL render a Loading_State using DaisyUI skeleton loaders
2. THE Loading_State SHALL match the layout structure of the loaded content
3. WHEN an error occurs during data fetching, THE Page_Component SHALL render an Error_State using DaisyUI alert component
4. THE Error_State SHALL display an error icon from Lucide
5. THE Error_State SHALL display translated error message using the Translation_System
6. THE Error_State SHALL provide a retry button when applicable
7. THE Loading_State SHALL use the Design_System colors and spacing
8. THE Error_State SHALL use the Design_System colors and spacing
9. THE Page_Component SHALL NOT modify existing error handling logic
10. THE Page_Component SHALL NOT modify existing loading state management

### Requirement 18: Icon Usage

**User Story:** As a developer, I want consistent icon usage, so that the interface has a cohesive visual language.

#### Acceptance Criteria

1. THE UI_System SHALL use Lucide React as the primary icon library
2. THE UI_System SHALL use React Icons only when specific icons are unavailable in Lucide
3. THE UI_System SHALL use consistent icon sizes: 14px for badges, 16px for buttons, 18px for nav items, 20px for mobile nav, 24px for empty states
4. THE UI_System SHALL use consistent icon stroke widths: 2 for normal, 2.5 for active states
5. THE UI_System SHALL use semantically appropriate icons for actions (Trash2 for delete, Edit for edit, Eye for view, Upload for upload)
6. THE UI_System SHALL use Building2 icon for Institute_Badge
7. THE UI_System SHALL use Sun icon for light theme and Moon icon for dark theme
8. THE UI_System SHALL use MessageSquarePlus icon for new chat
9. THE UI_System SHALL use AlertTriangle icon for delete confirmation
10. THE UI_System SHALL NOT mix icon libraries randomly within the same component

### Requirement 19: Accessibility

**User Story:** As a user with accessibility needs, I want the interface to be accessible, so that I can use assistive technologies effectively.

#### Acceptance Criteria

1. THE UI_System SHALL provide aria-label attributes for all icon-only buttons
2. THE UI_System SHALL provide aria-expanded attributes for collapsible elements
3. THE UI_System SHALL provide aria-controls attributes for elements that control other elements
4. THE UI_System SHALL ensure all interactive elements are keyboard accessible
5. THE UI_System SHALL provide visible focus indicators for keyboard navigation
6. THE UI_System SHALL use semantic HTML elements (nav, header, main, button, etc.)
7. THE UI_System SHALL provide alt text for all images
8. THE UI_System SHALL ensure color is not the only means of conveying information
9. THE Motion_System SHALL respect prefers-reduced-motion preference
10. THE UI_System SHALL maintain existing ARIA attributes and not remove them

### Requirement 20: Code Preservation

**User Story:** As a developer, I want all business logic preserved, so that the refactor doesn't break existing functionality.

#### Acceptance Criteria

1. THE UI_System SHALL NOT modify any files containing useQuery, useMutation, or useInfiniteQuery
2. THE UI_System SHALL NOT modify any files containing @isin/ service client imports
3. THE UI_System SHALL NOT modify any files containing useAuth, useOidc, or react-oidc-context hooks
4. THE UI_System SHALL NOT modify route definition files
5. THE UI_System SHALL NOT modify vite.config.ts, tsconfig*.json, or package.json
6. THE UI_System SHALL NOT modify any .env files
7. THE UI_System SHALL NOT restructure component file organization
8. THE UI_System SHALL NOT rename or remove existing props, state variables, or callbacks
9. THE UI_System SHALL NOT install new npm packages
10. THE UI_System SHALL preserve all existing event handlers and their wiring
11. THE UI_System SHALL preserve all existing data transformation functions
12. THE UI_System SHALL preserve all existing validation logic

