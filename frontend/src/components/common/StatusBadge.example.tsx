import { StatusBadge } from './StatusBadge';

/**
 * StatusBadge Component Examples
 * 
 * This file demonstrates various usage patterns for the StatusBadge component.
 */

export function StatusBadgeExamples() {
  return (
    <div className="space-y-8 p-6">
      {/* Auto-Detection Examples */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Auto-Detection</h2>
        <p className="text-base-content/70 mb-4">
          The component automatically determines the badge color based on status keywords.
        </p>
        <div className="flex flex-wrap gap-3">
          <StatusBadge status="active" />
          <StatusBadge status="success" />
          <StatusBadge status="completed" />
          <StatusBadge status="approved" />
          <StatusBadge status="available" />
        </div>
      </section>

      {/* Error States */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Error States</h2>
        <div className="flex flex-wrap gap-3">
          <StatusBadge status="error" />
          <StatusBadge status="failed" />
          <StatusBadge status="rejected" />
          <StatusBadge status="unavailable" />
        </div>
      </section>

      {/* Warning States */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Warning States</h2>
        <div className="flex flex-wrap gap-3">
          <StatusBadge status="pending" />
          <StatusBadge status="processing" />
          <StatusBadge status="in progress" />
          <StatusBadge status="warning" />
        </div>
      </section>

      {/* Info States */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Info States</h2>
        <div className="flex flex-wrap gap-3">
          <StatusBadge status="info" />
          <StatusBadge status="draft" />
          <StatusBadge status="new" />
        </div>
      </section>

      {/* Neutral States */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Neutral States</h2>
        <div className="flex flex-wrap gap-3">
          <StatusBadge status="inactive" />
          <StatusBadge status="archived" />
          <StatusBadge status="unknown" />
        </div>
      </section>

      {/* Explicit Variant Override */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Explicit Variant Override</h2>
        <p className="text-base-content/70 mb-4">
          You can explicitly set the variant to override auto-detection.
        </p>
        <div className="flex flex-wrap gap-3">
          <StatusBadge status="Custom Status" variant="success" />
          <StatusBadge status="In Review" variant="info" />
          <StatusBadge status="Blocked" variant="error" />
          <StatusBadge status="On Hold" variant="warning" />
          <StatusBadge status="Archived" variant="neutral" />
        </div>
      </section>

      {/* Real-World Usage Examples */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Real-World Usage</h2>
        <div className="space-y-4">
          {/* Adapter Status */}
          <div className="card bg-base-100 border border-base-content/10 p-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold">Model Adapter v2.1</h3>
                <p className="text-sm text-base-content/70">Fine-tuned model</p>
              </div>
              <StatusBadge status="active" />
            </div>
          </div>

          {/* Document Status */}
          <div className="card bg-base-100 border border-base-content/10 p-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold">Document Processing</h3>
                <p className="text-sm text-base-content/70">report.pdf</p>
              </div>
              <StatusBadge status="processing" />
            </div>
          </div>

          {/* Chat Status */}
          <div className="card bg-base-100 border border-base-content/10 p-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold">Chat Session</h3>
                <p className="text-sm text-base-content/70">AI Assistant</p>
              </div>
              <StatusBadge status="available" />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
