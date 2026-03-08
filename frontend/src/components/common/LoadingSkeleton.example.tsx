import { LoadingSkeleton } from './LoadingSkeleton';

/**
 * LoadingSkeleton Component Examples
 * 
 * This file demonstrates various usage patterns for the LoadingSkeleton component.
 */

export function LoadingSkeletonExamples() {
  return (
    <div className="space-y-12 p-8">
      {/* List Variant Example */}
      <section>
        <h2 className="mb-4 text-2xl font-bold">List Variant</h2>
        <p className="mb-4 text-base-content/70">
          Use for loading states in list views like documents, chats, or any vertical list layout.
        </p>
        <LoadingSkeleton variant="list" count={3} />
      </section>

      {/* Card Variant Example */}
      <section>
        <h2 className="mb-4 text-2xl font-bold">Card Variant</h2>
        <p className="mb-4 text-base-content/70">
          Use for loading states in card grid layouts like adapters, products, or dashboard widgets.
        </p>
        <LoadingSkeleton variant="card" count={6} />
      </section>

      {/* Table Variant Example */}
      <section>
        <h2 className="mb-4 text-2xl font-bold">Table Variant</h2>
        <p className="mb-4 text-base-content/70">
          Use for loading states in table layouts like user lists, data tables, or reports.
        </p>
        <LoadingSkeleton variant="table" count={5} />
      </section>

      {/* Custom Count Example */}
      <section>
        <h2 className="mb-4 text-2xl font-bold">Custom Count</h2>
        <p className="mb-4 text-base-content/70">
          Adjust the count prop to match your expected data size.
        </p>
        <LoadingSkeleton variant="list" count={8} />
      </section>
    </div>
  );
}

/**
 * Example: Using LoadingSkeleton in a Page Component
 */
export function DocumentsPageExample() {
  // Simulating loading state
  const isLoading = true;
  const documents = [];

  return (
    <div className="p-6">
      <h1 className="mb-6 text-3xl font-bold">Documents</h1>
      
      {isLoading ? (
        <LoadingSkeleton variant="list" count={5} />
      ) : documents.length === 0 ? (
        <div className="text-center text-base-content/60">
          No documents found
        </div>
      ) : (
        <div>
          {/* Document list would go here */}
        </div>
      )}
    </div>
  );
}

/**
 * Example: Using LoadingSkeleton in a Card Grid
 */
export function AdaptersPageExample() {
  // Simulating loading state
  const isLoading = true;
  const adapters = [];

  return (
    <div className="p-6">
      <h1 className="mb-6 text-3xl font-bold">Adapters</h1>
      
      {isLoading ? (
        <LoadingSkeleton variant="card" count={6} />
      ) : adapters.length === 0 ? (
        <div className="text-center text-base-content/60">
          No adapters found
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {/* Adapter cards would go here */}
        </div>
      )}
    </div>
  );
}

/**
 * Example: Using LoadingSkeleton in a Table
 */
export function UsersTableExample() {
  // Simulating loading state
  const isLoading = true;
  const users = [];

  return (
    <div className="p-6">
      <h1 className="mb-6 text-3xl font-bold">Users</h1>
      
      {isLoading ? (
        <LoadingSkeleton variant="table" count={10} />
      ) : users.length === 0 ? (
        <div className="text-center text-base-content/60">
          No users found
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="table w-full">
            {/* Table content would go here */}
          </table>
        </div>
      )}
    </div>
  );
}
