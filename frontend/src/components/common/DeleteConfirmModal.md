# DeleteConfirmModal Component

A reusable confirmation dialog for destructive actions.

## Features

- Uses DaisyUI modal component as the base
- Renders dark overlay with backdrop blur
- Displays AlertTriangle icon in error/red color
- Shows translated title and message
- Supports optional itemName for personalized messages
- Animates entrance with Framer Motion (scale 0.95→1, opacity 0→1)
- Handles Escape key and overlay click to close
- Prevents background scroll when open
- Provides Cancel and Delete buttons with proper callbacks

## Props

```typescript
interface DeleteConfirmModalProps {
  isOpen: boolean;        // Controls modal visibility
  onConfirm: () => void;  // Callback when Delete button is clicked
  onCancel: () => void;   // Callback when Cancel button is clicked or modal is dismissed
  itemName?: string;      // Optional item name for personalized message
}
```

## Usage

### Basic Usage

```tsx
import { useState } from 'react';
import { DeleteConfirmModal } from '@/components/common';

function MyComponent() {
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  const handleDelete = () => {
    // Perform deletion logic here
    console.log('Item deleted');
    setIsDeleteModalOpen(false);
  };

  return (
    <>
      <button onClick={() => setIsDeleteModalOpen(true)}>
        Delete Item
      </button>

      <DeleteConfirmModal
        isOpen={isDeleteModalOpen}
        onConfirm={handleDelete}
        onCancel={() => setIsDeleteModalOpen(false)}
      />
    </>
  );
}
```

### With Item Name

```tsx
import { useState } from 'react';
import { DeleteConfirmModal } from '@/components/common';

function DocumentList() {
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);

  const handleDeleteClick = (documentName: string) => {
    setSelectedDocument(documentName);
    setIsDeleteModalOpen(true);
  };

  const handleConfirmDelete = () => {
    if (selectedDocument) {
      // Perform deletion logic here
      console.log(`Deleting document: ${selectedDocument}`);
      setIsDeleteModalOpen(false);
      setSelectedDocument(null);
    }
  };

  const handleCancelDelete = () => {
    setIsDeleteModalOpen(false);
    setSelectedDocument(null);
  };

  return (
    <>
      <button onClick={() => handleDeleteClick('My Document.pdf')}>
        Delete Document
      </button>

      <DeleteConfirmModal
        isOpen={isDeleteModalOpen}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        itemName={selectedDocument || undefined}
      />
    </>
  );
}
```

## Translation Keys

The component uses the following translation keys:

- `modal.delete.title` - Modal title
- `modal.delete.message` - Generic confirmation message
- `modal.delete.messageNamed` - Confirmation message with item name (uses `{{itemName}}` placeholder)
- `modal.delete.confirm` - Delete button label
- `modal.delete.cancel` - Cancel button label

## Accessibility

- Uses semantic HTML with proper ARIA attributes
- Supports keyboard navigation (Escape key to close)
- Prevents background scroll when open
- Provides proper focus management
- Uses aria-label and aria-describedby for screen readers

## Requirements Satisfied

- 7.1: Display before executing deletion
- 7.2: Use DaisyUI modal component
- 7.3: Render dark overlay with backdrop blur
- 7.4: Freeze background page
- 7.5: Display AlertTriangle icon
- 7.6: Display translated title
- 7.7: Display translated message
- 7.8: Display translated message with item name when provided
- 7.9: Render Cancel button
- 7.10: Render Delete button
- 7.11: Animate entrance with Framer Motion
- 7.12: Close on overlay click
- 7.13: Close on Escape key
- 7.14: Accept isOpen, onConfirm, onCancel, and itemName props
- 16.1: Reusable component
- 16.8: Pure presentation component
