import { useEffect } from 'react';
import { AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useTranslation } from 'react-i18next';

interface DeleteConfirmModalProps {
  isOpen: boolean;
  onConfirm: () => void;
  onCancel: () => void;
  itemName?: string;
}

/**
 * DeleteConfirmModal Component
 * 
 * A reusable confirmation dialog for destructive actions.
 * 
 * Features:
 * - Uses DaisyUI modal component as the base
 * - Renders dark overlay with backdrop blur
 * - Displays AlertTriangle icon in error/red color
 * - Shows translated title and message
 * - Supports optional itemName for personalized messages
 * - Animates entrance with Framer Motion (scale 0.95→1, opacity 0→1)
 * - Handles Escape key and overlay click to close
 * - Prevents background scroll when open
 * - Provides Cancel and Delete buttons with proper callbacks
 * 
 * Requirements satisfied:
 * - 7.1: Display before executing deletion
 * - 7.2: Use DaisyUI modal component
 * - 7.3: Render dark overlay with backdrop blur
 * - 7.4: Freeze background page
 * - 7.5: Display AlertTriangle icon
 * - 7.6: Display translated title
 * - 7.7: Display translated message
 * - 7.8: Display translated message with item name when provided
 * - 7.9: Render Cancel button
 * - 7.10: Render Delete button
 * - 7.11: Animate entrance with Framer Motion
 * - 7.12: Close on overlay click
 * - 7.13: Close on Escape key
 * - 7.14: Accept isOpen, onConfirm, onCancel, and itemName props
 * - 16.1: Reusable component
 * - 16.8: Pure presentation component
 */
export function DeleteConfirmModal({
  isOpen,
  onConfirm,
  onCancel,
  itemName,
}: DeleteConfirmModalProps) {
  const { t } = useTranslation();

  // Handle Escape key press
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onCancel();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      // Prevent background scroll
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onCancel]);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
            onClick={onCancel}
            aria-hidden="true"
          />

          {/* Modal content */}
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.2 }}
              className="modal-box relative max-w-md rounded-2xl bg-base-100 p-6 shadow-xl"
              role="dialog"
              aria-modal="true"
              aria-labelledby="modal-title"
              aria-describedby="modal-description"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Icon */}
              <div className="mb-4 flex justify-center">
                <div className="rounded-full bg-error/10 p-3">
                  <AlertTriangle
                    size={32}
                    className="text-error"
                    strokeWidth={2}
                    aria-hidden="true"
                  />
                </div>
              </div>

              {/* Title */}
              <h3
                id="modal-title"
                className="mb-2 text-center text-xl font-semibold text-base-content"
              >
                {t('modal.delete.title')}
              </h3>

              {/* Message */}
              <p
                id="modal-description"
                className="mb-6 text-center text-base-content/70"
              >
                {itemName
                  ? t('modal.delete.messageNamed', { itemName })
                  : t('modal.delete.message')}
              </p>

              {/* Action buttons */}
              <div className="flex gap-3">
                <button
                  onClick={onCancel}
                  className="btn btn-ghost flex-1"
                  type="button"
                >
                  {t('modal.delete.cancel')}
                </button>
                <button
                  onClick={onConfirm}
                  className="btn btn-error flex-1"
                  type="button"
                >
                  {t('modal.delete.confirm')}
                </button>
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
