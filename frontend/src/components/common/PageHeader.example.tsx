import { PageHeader } from './PageHeader';
import { FileText, Upload, MessageSquare, MessageSquarePlus, Settings, Cpu } from 'lucide-react';

/**
 * PageHeader Component Examples
 * 
 * This file demonstrates various usage patterns for the PageHeader component.
 */

export function PageHeaderExamples() {
  return (
    <div className="space-y-8 p-6">
      <h2 className="text-2xl font-bold">PageHeader Component Examples</h2>

      {/* Example 1: Basic header with title only */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Basic Header (Title Only)</h3>
        <PageHeader title="Settings" />
      </div>

      {/* Example 2: Header with icon and title */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Header with Icon</h3>
        <PageHeader
          icon={Settings}
          title="Settings"
        />
      </div>

      {/* Example 3: Header with icon, title, and subtitle */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Header with Icon and Subtitle</h3>
        <PageHeader
          icon={FileText}
          title="Documents"
          subtitle="Manage your PDF documents"
        />
      </div>

      {/* Example 4: Header with action button (no icon) */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Header with Action Button</h3>
        <PageHeader
          icon={MessageSquare}
          title="Chats"
          subtitle="Your conversation history"
          action={{
            label: "New Chat",
            onClick: () => console.log('New chat clicked'),
          }}
        />
      </div>

      {/* Example 5: Header with action button with icon */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Header with Action Button and Icon</h3>
        <PageHeader
          icon={FileText}
          title="Documents"
          subtitle="Upload and manage your PDF files"
          action={{
            label: "Upload Document",
            icon: Upload,
            onClick: () => console.log('Upload clicked'),
          }}
        />
      </div>

      {/* Example 6: Chat page header */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Chat Page Header</h3>
        <PageHeader
          icon={MessageSquare}
          title="Chats"
          subtitle="Your conversation history"
          action={{
            label: "New Chat",
            icon: MessageSquarePlus,
            onClick: () => console.log('New chat clicked'),
          }}
        />
      </div>

      {/* Example 7: Adapters page header */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Adapters Page Header</h3>
        <PageHeader
          icon={Cpu}
          title="Adapters"
          subtitle="Manage your model adapters"
        />
      </div>

      {/* Example 8: Long title and subtitle */}
      <div>
        <h3 className="mb-4 text-lg font-semibold">Long Title and Subtitle</h3>
        <PageHeader
          icon={FileText}
          title="Document Management System"
          subtitle="Upload, organize, and manage all your important PDF documents in one centralized location"
          action={{
            label: "Upload New Document",
            icon: Upload,
            onClick: () => console.log('Upload clicked'),
          }}
        />
      </div>
    </div>
  );
}
