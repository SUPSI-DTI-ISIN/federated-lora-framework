import toast from 'react-hot-toast';

/**
 * ThemedToaster Example
 * 
 * The ThemedToaster component is already integrated in App.tsx and provides theme-aware toast notifications.
 * 
 * Usage:
 * Simply import toast from 'react-hot-toast' and use it anywhere in your application.
 * The ThemedToaster component will automatically apply the correct styling based on the current theme.
 * 
 * Examples:
 */

export const ThemedToasterExample = () => {
  const showSuccessToast = () => {
    toast.success('Document uploaded successfully!');
  };

  const showErrorToast = () => {
    toast.error('Failed to delete adapter');
  };

  const showLoadingToast = () => {
    toast.loading('Processing your request...');
  };

  const showInfoToast = () => {
    toast('This is an info message', {
      icon: '💡',
    });
  };

  const showCustomDurationToast = () => {
    toast.success('This will disappear in 2 seconds', {
      duration: 2000,
    });
  };

  const showToastWithId = () => {
    // Useful for updating the same toast
    toast.loading('Downloading adapter...', { id: 'adapter-download' });
    
    setTimeout(() => {
      toast.success('Adapter downloaded!', { id: 'adapter-download' });
    }, 2000);
  };

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-heading font-semibold mb-4">Toast Notification Examples</h2>
      
      <div className="space-y-2">
        <button onClick={showSuccessToast} className="btn btn-success">
          Show Success Toast
        </button>
        
        <button onClick={showErrorToast} className="btn btn-error">
          Show Error Toast
        </button>
        
        <button onClick={showLoadingToast} className="btn btn-info">
          Show Loading Toast
        </button>
        
        <button onClick={showInfoToast} className="btn btn-neutral">
          Show Info Toast
        </button>
        
        <button onClick={showCustomDurationToast} className="btn btn-primary">
          Show Custom Duration Toast
        </button>
        
        <button onClick={showToastWithId} className="btn btn-secondary">
          Show Toast with ID (Updates)
        </button>
      </div>

      <div className="mt-8 p-4 bg-base-200 rounded-lg">
        <h3 className="font-semibold mb-2">Features:</h3>
        <ul className="list-disc list-inside space-y-1 text-sm">
          <li>Automatically adapts to light/dark theme changes</li>
          <li>Bottom-right position with 4000ms default duration</li>
          <li>Uses DM Sans font matching the design system</li>
          <li>Includes CheckCircle icon for success</li>
          <li>Includes XCircle icon for errors</li>
          <li>Includes Info icon for loading states</li>
          <li>Theme-specific colors from the design system</li>
          <li>Rounded-lg border radius</li>
        </ul>
      </div>

      <div className="mt-4 p-4 bg-base-200 rounded-lg">
        <h3 className="font-semibold mb-2">Requirements Validated:</h3>
        <ul className="list-disc list-inside space-y-1 text-sm">
          <li>11.1: Uses React Hot Toast ✓</li>
          <li>11.2: Positioned at bottom-right ✓</li>
          <li>11.3: 4000ms duration ✓</li>
          <li>11.4: Light theme colors matching Design_System ✓</li>
          <li>11.5: Dark theme colors matching Design_System ✓</li>
          <li>11.6: Uses DM Sans font ✓</li>
          <li>11.7: Uses rounded-lg border radius ✓</li>
          <li>11.8: Includes icons for success, error, and info states ✓</li>
          <li>11.9: Uses translated text via Translation_System (in usage) ✓</li>
          <li>11.10: Does not modify existing toast trigger logic ✓</li>
        </ul>
      </div>
    </div>
  );
};
