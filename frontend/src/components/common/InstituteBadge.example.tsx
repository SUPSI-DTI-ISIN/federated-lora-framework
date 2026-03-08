import { InstituteBadge } from './InstituteBadge';

/**
 * InstituteBadge Component Examples
 * 
 * This file demonstrates various usage scenarios for the InstituteBadge component.
 */

export function InstituteBadgeExamples() {
  return (
    <div className="space-y-8 p-8">
      <div>
        <h2 className="text-2xl font-bold mb-4">InstituteBadge Examples</h2>
        <p className="text-base-content/70 mb-6">
          A reusable badge component for displaying institute names in the navbar.
        </p>
      </div>

      {/* Short Name */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Short Name (No Truncation)</h3>
        <p className="text-sm text-base-content/70 mb-2">
          Names with 20 or fewer characters display fully without truncation.
        </p>
        <div className="flex gap-4 flex-wrap">
          <InstituteBadge instituteName="MIT" />
          <InstituteBadge instituteName="Stanford" />
          <InstituteBadge instituteName="University of Tech" />
        </div>
      </div>

      {/* Medium Name */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Medium Name (At Threshold)</h3>
        <p className="text-sm text-base-content/70 mb-2">
          Names with exactly 20 characters display fully.
        </p>
        <div className="flex gap-4 flex-wrap">
          <InstituteBadge instituteName="University of Oxford" />
          <InstituteBadge instituteName="Cambridge University" />
        </div>
      </div>

      {/* Long Name with Truncation */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Long Name (With Truncation & Tooltip)</h3>
        <p className="text-sm text-base-content/70 mb-2">
          Names longer than 20 characters are truncated with ellipsis. Hover to see the full name in a tooltip.
        </p>
        <div className="flex gap-4 flex-wrap">
          <InstituteBadge instituteName="Massachusetts Institute of Technology" />
          <InstituteBadge instituteName="California Institute of Technology and Research" />
          <InstituteBadge instituteName="The Royal Institute of Advanced Studies and Research" />
        </div>
      </div>

      {/* Theme Demonstration */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Theme Support</h3>
        <p className="text-sm text-base-content/70 mb-2">
          The badge automatically adapts to light and dark themes with indigo color variants.
        </p>
        <div className="flex gap-4 flex-wrap">
          <InstituteBadge instituteName="University of Technology" />
          <InstituteBadge instituteName="Institute of Science" />
        </div>
        <p className="text-xs text-base-content/60 mt-2">
          Toggle the theme to see the color changes.
        </p>
      </div>

      {/* With Custom Styling */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">With Custom Styling</h3>
        <p className="text-sm text-base-content/70 mb-2">
          Additional CSS classes can be applied via the className prop.
        </p>
        <div className="flex gap-4 flex-wrap items-center">
          <InstituteBadge instituteName="Default Styling" />
          <InstituteBadge instituteName="With Margin" className="ml-4" />
          <InstituteBadge instituteName="With Shadow" className="shadow-lg" />
        </div>
      </div>

      {/* In Context (Navbar Simulation) */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">In Navbar Context</h3>
        <p className="text-sm text-base-content/70 mb-2">
          Example of how the badge appears in a navbar layout.
        </p>
        <div className="border border-base-content/10 rounded-lg p-4 bg-base-100">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-primary rounded-full" />
              <span className="font-bold">App Logo</span>
            </div>
            <InstituteBadge instituteName="University of Technology" />
            <div className="flex-1" />
            <div className="text-sm text-base-content/70">Other Nav Items →</div>
          </div>
        </div>
      </div>

      {/* Accessibility Notes */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">Accessibility Features</h3>
        <ul className="list-disc list-inside text-sm text-base-content/70 space-y-1">
          <li>Uses semantic <code>role="status"</code> attribute</li>
          <li>Includes <code>aria-label</code> with full institute name</li>
          <li>Icon has <code>aria-hidden="true"</code> to prevent duplication</li>
          <li>Tooltip provides full text for truncated names</li>
          <li>Not interactive (no focus or click handlers)</li>
        </ul>
      </div>
    </div>
  );
}

export default InstituteBadgeExamples;
