import { useState } from 'react';
import { DeleteConfirmModal } from './DeleteConfirmModal';
import { Trash2 } from 'lucide-react';

/**
 * Example usage of DeleteConfirmModal component
 * 
 * This file demonstrates how to integrate the DeleteConfirmModal
 * into your components for handling destructive actions.
 */
export function DeleteConfirmModalExample() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [itemToDelete, setItemToDelete] = useState<string | null>(null);

  // Example: Delete without item name
  const handleSimpleDelete = () => {
    setItemToDelete(null);
    setIsModalOpen(true);
  };

  // Example: Delete with item name
  const handleNamedDelete = (name: string) => {
    setItemToDelete(name);
    setIsModalOpen(true);
  };

  const handleConfirmDelete = () => {
    console.log('Deleting:', itemToDelete || 'unnamed item');
    // Add your deletion logic here
    // e.g., call API, update state, show toast notification
    setIsModalOpen(false);
    setItemToDelete(null);
  };

  const handleCancelDelete = () => {
    setIsModalOpen(false);
    setItemToDelete(null);
  };

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold">DeleteConfirmModal Examples</h2>

      {/* Example 1: Simple delete without item name */}
      <div className="card bg-base-200 p-4">
        <h3 className="font-semibold mb-2">Example 1: Generic Delete</h3>
        <p className="text-sm text-base-content/70 mb-4">
          Delete action without specifying an item name
        </p>
        <button
          onClick={handleSimpleDelete}
          className="btn btn-error btn-sm"
        >
          <Trash2 size={16} />
          Delete Item
        </button>
      </div>

      {/* Example 2: Delete with item name */}
      <div className="card bg-base-200 p-4">
        <h3 className="font-semibold mb-2">Example 2: Named Delete</h3>
        <p className="text-sm text-base-content/70 mb-4">
          Delete action with a specific item name
        </p>
        <div className="flex gap-2">
          <button
            onClick={() => handleNamedDelete('Document.pdf')}
            className="btn btn-error btn-sm"
          >
            <Trash2 size={16} />
            Delete Document.pdf
          </button>
          <button
            onClick={() => handleNamedDelete('My Important File.docx')}
            className="btn btn-error btn-sm"
          >
            <Trash2 size={16} />
            Delete My Important File.docx
          </button>
        </div>
      </div>

      {/* Example 3: Delete from a list */}
      <div className="card bg-base-200 p-4">
        <h3 className="font-semibold mb-2">Example 3: Delete from List</h3>
        <p className="text-sm text-base-content/70 mb-4">
          Typical use case in a list of items
        </p>
        <div className="space-y-2">
          {['Report Q1.pdf', 'Meeting Notes.txt', 'Budget 2024.xlsx'].map((item) => (
            <div
              key={item}
              className="flex items-center justify-between p-3 bg-base-100 rounded-lg"
            >
              <span className="text-sm">{item}</span>
              <button
                onClick={() => handleNamedDelete(item)}
                className="btn btn-ghost btn-sm btn-circle"
                aria-label={`Delete ${item}`}
              >
                <Trash2 size={16} className="text-error" />
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* The modal */}
      <DeleteConfirmModal
        isOpen={isModalOpen}
        onConfirm={handleConfirmDelete}
        onCancel={handleCancelDelete}
        itemName={itemToDelete || undefined}
      />
    </div>
  );
}
