import { MessageSquare, FileText, Plug, Upload } from 'lucide-react';
import { EmptyState } from './EmptyState';

/**
 * EmptyState Component Examples
 * 
 * This file demonstrates various usage patterns for the EmptyState component.
 */

// Example 1: Basic empty state without action
export function BasicEmptyStateExample() {
  return (
    <EmptyState
      icon={MessageSquare}
      title="No chats yet"
      description="Start a new conversation to get started"
    />
  );
}

// Example 2: Empty state with action button
export function EmptyStateWithActionExample() {
  const handleUpload = () => {
    console.log('Upload clicked');
  };

  return (
    <EmptyState
      icon={FileText}
      title="No documents"
      description="Upload your first PDF document to get started"
      action={{
        label: "Upload Document",
        onClick: handleUpload
      }}
    />
  );
}

// Example 3: Empty state without description
export function EmptyStateNoDescriptionExample() {
  const handleCreate = () => {
    console.log('Create clicked');
  };

  return (
    <EmptyState
      icon={Plug}
      title="No adapters configured"
      action={{
        label: "Create Adapter",
        onClick: handleCreate
      }}
    />
  );
}

// Example 4: Empty state for documents with upload icon
export function DocumentsEmptyStateExample() {
  const handleUpload = () => {
    console.log('Upload clicked');
  };

  return (
    <EmptyState
      icon={Upload}
      title="No documents uploaded"
      description="Drag and drop files here or click the button below to upload"
      action={{
        label: "Choose Files",
        onClick: handleUpload
      }}
    />
  );
}

// Example 5: Empty state in a page layout
export function EmptyStateInPageExample() {
  const handleNewChat = () => {
    console.log('New chat clicked');
  };

  return (
    <div className="container mx-auto p-6">
      <h1 className="mb-6 text-2xl font-bold">Chats</h1>
      <EmptyState
        icon={MessageSquare}
        title="No conversations yet"
        description="Create your first chat to start a conversation with the AI assistant"
        action={{
          label: "New Chat",
          onClick: handleNewChat
        }}
      />
    </div>
  );
}
