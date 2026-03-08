import { NavigationShell } from "./NavigationShell";

/**
 * Example: Basic Usage
 * 
 * Wrap your page content with NavigationShell to get the full layout structure
 * including navbar, sidebar, and responsive behavior.
 */
export function BasicUsageExample() {
  return (
    <NavigationShell>
      <div className="space-y-6">
        <h1 className="text-3xl font-bold">Page Title</h1>
        <p className="text-base-content/70">
          This content is automatically wrapped with the navigation shell,
          providing consistent layout across all pages.
        </p>
      </div>
    </NavigationShell>
  );
}

/**
 * Example: With Page Content
 * 
 * The NavigationShell provides proper spacing and container constraints,
 * so your content is automatically centered and responsive.
 */
export function WithPageContentExample() {
  return (
    <NavigationShell>
      <div className="space-y-8">
        {/* Page Header */}
        <div>
          <h1 className="text-3xl font-bold mb-2">Documents</h1>
          <p className="text-base-content/70">
            Manage your PDF documents and sections
          </p>
        </div>

        {/* Page Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="card bg-base-200 p-6">
              <h3 className="font-semibold mb-2">Document {i}</h3>
              <p className="text-sm text-base-content/70">
                Sample document content
              </p>
            </div>
          ))}
        </div>
      </div>
    </NavigationShell>
  );
}

/**
 * Example: Responsive Behavior
 * 
 * The NavigationShell automatically handles responsive behavior:
 * - Desktop (≥1280px): Full sidebar with icons and labels (w-64)
 * - Tablet (≥768px-1279px): Icon-only sidebar (w-16) with tooltips
 * - Mobile (<768px): Drawer overlay triggered by hamburger menu
 * 
 * Content padding also adjusts:
 * - Desktop: p-6 (24px)
 * - Mobile: p-4 (16px)
 */
export function ResponsiveBehaviorExample() {
  return (
    <NavigationShell>
      <div className="space-y-6">
        <h1 className="text-2xl md:text-3xl lg:text-4xl font-bold">
          Responsive Content
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="card bg-base-200 p-4">
            <p className="text-sm">
              On mobile, the sidebar is hidden and accessible via drawer
            </p>
          </div>
          <div className="card bg-base-200 p-4">
            <p className="text-sm">
              On tablet, the sidebar shows icons only with tooltips
            </p>
          </div>
          <div className="card bg-base-200 p-4">
            <p className="text-sm">
              On desktop, the sidebar shows full icons and labels
            </p>
          </div>
        </div>
      </div>
    </NavigationShell>
  );
}

/**
 * Example: Integration with App Router
 * 
 * Typically used in App.tsx to wrap all routes
 */
export function AppIntegrationExample() {
  return (
    <NavigationShell>
      {/* Your router outlet or page content goes here */}
      <div>
        <h1>Current Page Content</h1>
        <p>This will be replaced by your actual page components</p>
      </div>
    </NavigationShell>
  );
}
