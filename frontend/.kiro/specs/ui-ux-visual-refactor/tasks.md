# Implementation Plan: UI/UX Visual Refactor

## Overview

This implementation plan transforms the React + TypeScript frontend into a modern, enterprise-grade SaaS interface using Tailwind CSS v4, DaisyUI v5, Framer Motion v12, and Lucide React. The refactor focuses exclusively on visual presentation while preserving all business logic, API integrations, authentication flows, and component structure.

## Tasks

- [x] 1. Configure design system foundation
  - Update Tailwind CSS v4 configuration with custom theme colors, fonts, and design tokens
  - Configure DaisyUI v5 with light and dark theme definitions
  - Add Google Fonts imports for Plus Jakarta Sans, DM Sans, and JetBrains Mono
  - Define custom CSS variables for theme-specific colors in both light and dark modes
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10_

- [ ] 2. Implement theme management system
  - [x] 2.1 Create ThemeToggle component with localStorage persistence
    - Implement theme detection from localStorage and OS preference
    - Add Sun/Moon icon toggle with Framer Motion AnimatePresence
    - Update html data-theme attribute on theme change
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8_
  
  - [x] 2.2 Create theme context/provider (if needed)
    - Provide theme state to components that need dynamic styling
    - _Requirements: 2.1, 2.2, 2.3_

- [ ] 3. Build reusable UI component library
  - [x] 3.1 Create DeleteConfirmModal component
    - Implement DaisyUI modal with dark overlay and backdrop blur
    - Add AlertTriangle icon, translated title and message
    - Wire Cancel and Delete buttons with proper callbacks
    - Add Framer Motion entrance animation (scale 0.95→1, opacity 0→1)
    - Handle Escape key and overlay click to close
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.12, 7.13, 7.14, 16.1, 16.8_
  
  - [x] 3.2 Create PageHeader component
    - Accept icon, title, subtitle, and optional action button props
    - Use Design_System typography and spacing
    - _Requirements: 16.2, 16.9_
  
  - [x] 3.3 Create EmptyState component
    - Accept icon, title, description, and optional CTA props
    - Center content with generous whitespace
    - _Requirements: 16.3, 16.10_
  
  - [x] 3.4 Create LoadingSkeleton component
    - Implement variants for list, card, and table layouts
    - Use DaisyUI skeleton component with theme-appropriate colors
    - _Requirements: 16.4, 16.11, 17.1, 17.2, 17.7_
  
  - [x] 3.5 Create StatusBadge component
    - Map status values to DaisyUI badge colors (success, error, warning, info, neutral)
    - Use rounded-full border radius
    - _Requirements: 16.5, 16.12_
  
  - [x] 3.6 Create InstituteBadge component
    - Display INSTITUTE_NAME with Building2 icon
    - Apply theme-specific indigo colors (light: border-indigo-200 bg-indigo-50 text-indigo-700, dark: border-indigo-700 bg-indigo-950 text-indigo-300)
    - Truncate long names with ellipsis and show tooltip
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 16.7, 16.14_

- [ ] 4. Implement navigation shell structure
  - [x] 4.1 Create NavigationShell layout wrapper
    - Implement top navbar with h-16 sticky positioning
    - Implement sidebar with w-64 on desktop, w-16 on tablet, drawer on mobile
    - Implement main content area with max-w-screen-2xl container
    - Add responsive padding (p-6 desktop, p-4 mobile)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.8, 3.9, 9.5, 9.6, 9.7, 9.8, 9.9_
  
  - [x] 4.2 Implement sidebar collapse and drawer logic
    - Add state management for sidebarCollapsed and drawerOpen
    - Animate sidebar width transitions with Framer Motion (duration 0.3s, easeInOut)
    - Handle drawer overlay with background scroll prevention
    - Close drawer on overlay click or Escape key
    - _Requirements: 3.7, 6.5, 6.6, 6.8, 6.9, 6.10, 10.6_
  
  - [x] 4.3 Build top navbar components
    - Add hamburger/collapse toggle button (leftmost)
    - Add app logo and name
    - Add InstituteBadge component
    - Add language switcher
    - Add ThemeToggle component
    - Add user avatar/profile dropdown menu (rightmost)
    - Wire hamburger to toggle sidebar/drawer based on viewport
    - Wire logout option to existing OIDC logout function
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10_
  
  - [x] 4.4 Implement sidebar navigation items
    - Map navigation items to existing routes with Lucide icons
    - Use Translation_System for all labels
    - Highlight active route with indigo left-border and subtle background
    - Show icon-only with tooltips when collapsed
    - Show icon + label when expanded
    - Add sidebar footer with app version or branding
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_

- [x] 5. Update internationalization files
  - Add translation keys for common actions (loading, error, retry, cancel, save, delete, edit, view, upload)
  - Add translation keys for modal.delete (title, message, messageNamed, confirm, cancel)
  - Add translation keys for navigation (home, documents, chats, adapters, settings, logout)
  - Add translation keys for theme toggle (light, dark)
  - Add translation keys for all page-specific content (home, documents, chats, adapters)
  - Update both en/translations.json and it/translations.json
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 8.10, 8.11, 8.12_

- [x] 6. Configure toast notification styling
  - Configure React Hot Toast with bottom-right position and 4000ms duration
  - Apply theme-specific colors matching Design_System
  - Use DM Sans font and rounded-lg border radius
  - Add appropriate icons for success, error, and info states
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 11.10_

- [x] 7. Refactor Home page visual presentation
  - Wrap page in motion.div with entrance animation (y: 12→0, opacity: 0→1, duration: 0.25s)
  - Render welcome hero section with greeting using t('home.welcome') and user name
  - Display summary stat cards using DaisyUI stats component when user data available
  - Render empty state with app logo, t('home.tagline'), and t('home.description') when no data
  - Apply centered layout with generous whitespace and indigo accent colors
  - Ensure full responsiveness across all viewport sizes
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 12.10, 10.2, 10.9_

- [ ] 8. Refactor Documents page visual presentation
  - [x] 8.1 Implement Documents page header and upload UI
    - Wrap page in motion.div with entrance animation
    - Render PageHeader with t('documents.title'), t('documents.subtitle'), and upload button
    - Style upload button with Upload icon and t('documents.upload') label
    - Create drag-and-drop zone with dashed indigo border and cloud upload icon
    - Display translated hint text in upload zone
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 10.2, 10.9_
  
  - [x] 8.2 Implement Documents list and states
    - Render document list as table or card grid with name, type badge, date, size, and actions
    - Create PDF badge in red/accent color
    - Render View and Delete action buttons as icon buttons
    - Wire Delete button to trigger DeleteConfirmModal
    - Render EmptyState with t('documents.empty') when no documents
    - Render LoadingSkeleton when data is loading
    - Render DaisyUI alert with error icon and t('documents.error') on error
    - _Requirements: 13.5, 13.6, 13.7, 13.8, 13.9, 13.10, 13.11, 13.12, 13.13, 13.14, 13.15, 17.1, 17.2, 17.3, 17.4, 17.5_

- [x] 9. Refactor Chat page visual presentation
  - Wrap page in motion.div with entrance animation
  - Render PageHeader with t('chats.title'), t('chats.subtitle'), and New Chat button
  - Style New Chat button with MessageSquarePlus icon
  - Render chat list as card-based layout with title/preview, timestamp, and right-arrow
  - Apply subtle lift animation on card hover using Motion_System
  - Wire chat card click to navigate to existing chat detail route
  - Add Trash2 icon button on each card wired to DeleteConfirmModal
  - Render EmptyState with MessageSquare icon and t('chats.empty') when no chats
  - Render LoadingSkeleton cards when data is loading
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 14.10, 14.11, 14.12, 14.13, 10.2, 10.5, 10.9_

- [x] 10. Refactor Adapters page visual presentation
  - Wrap page in motion.div with entrance animation
  - Render PageHeader with t('adapters.title') and t('adapters.subtitle')
  - Render adapters as card grid with name, StatusBadge, type/category, and action buttons
  - Use green badge for active status, grey badge for inactive status
  - Render Edit and Delete action buttons
  - Wire Delete button to trigger DeleteConfirmModal
  - Render EmptyState with Plug or Cpu icon and t('adapters.empty') when no adapters
  - Render LoadingSkeleton cards when data is loading
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7, 15.8, 15.9, 15.10, 15.11, 15.12, 15.13, 10.2, 10.9_

- [x] 11. Implement animation system enhancements
  - Add list stagger animations with staggerChildren: 0.05s for document, chat, and adapter lists
  - Add card hover animations (y: -2px) with shadow increase
  - Wrap modals in AnimatePresence for entrance/exit transitions
  - Add prefers-reduced-motion detection to disable/reduce animations when set
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 10.10_

- [x] 12. Add accessibility attributes
  - Add aria-label attributes for all icon-only buttons
  - Add aria-expanded attributes for collapsible sidebar and dropdowns
  - Add aria-controls attributes for hamburger toggle and drawer
  - Ensure visible focus indicators for keyboard navigation
  - Verify semantic HTML usage (nav, header, main, button)
  - Add alt text for any images
  - Ensure minimum 44x44px touch targets on mobile
  - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7, 19.8, 19.9, 19.10, 9.10_

- [x] 13. Final checkpoint - Verify all requirements
  - Test theme toggle functionality and persistence
  - Test responsive behavior at all breakpoints (320px, 768px, 1280px, 1920px)
  - Test sidebar collapse/expand and drawer overlay
  - Test delete confirmation modal on all pages
  - Verify all UI text uses Translation_System
  - Verify INSTITUTE_NAME displays correctly in navbar
  - Test keyboard navigation and accessibility
  - Verify all animations respect prefers-reduced-motion
  - Ensure no business logic, API calls, or routing was modified
  - Ensure all tests pass, ask the user if questions arise

## Notes

- All tasks preserve existing business logic, API integrations, authentication flows, and component structure
- No new npm packages will be installed - all libraries are already in package.json
- All UI text must use react-i18next t() function for internationalization
- Every delete action must be guarded by DeleteConfirmModal
- INSTITUTE_NAME must always be visible in navbar via InstituteBadge
- Theme toggle must be present and functional in navbar
- All pages must be fully responsive (≥320px, ≥768px, ≥1280px, ≥1920px)
- Animations must respect prefers-reduced-motion preference
- All interactive elements must have minimum 44x44px touch targets on mobile
- Focus on visual presentation only - do not modify hooks, API calls, routing, or state management
