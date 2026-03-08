import { useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { CheckCircle, XCircle, Info } from 'lucide-react';

export const ThemedToaster = () => {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    return (document.documentElement.getAttribute('data-theme') as 'light' | 'dark') || 'light';
  });

  useEffect(() => {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-theme') {
          const newTheme = document.documentElement.getAttribute('data-theme') as 'light' | 'dark';
          setTheme(newTheme || 'light');
        }
      });
    });

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme'],
    });

    return () => observer.disconnect();
  }, []);

  const colors = {
    light: {
      background: '#FFFFFF',
      text: '#1E293B',
      border: '#E2E8F0',
      success: '#10b981',
      error: '#ef4444',
      info: '#0ea5e9',
    },
    dark: {
      background: '#1A1D27',
      text: '#F8FAFC',
      border: '#334155',
      success: '#34d399',
      error: '#f87171',
      info: '#38bdf8',
    },
  };

  const currentColors = colors[theme];

  return (
    <Toaster
      position="bottom-right"
      toastOptions={{
        duration: 4000,
        style: {
          fontFamily: '"DM Sans", system-ui, sans-serif',
          borderRadius: '0.5rem',
          fontSize: '0.875rem',
          fontWeight: '500',
          padding: '12px 16px',
          maxWidth: '400px',
        },
        success: {
          icon: <CheckCircle size={20} />,
          style: {
            background: currentColors.background,
            color: currentColors.success,
            border: `1px solid ${currentColors.border}`,
          },
          iconTheme: {
            primary: currentColors.success,
            secondary: currentColors.background,
          },
        },
        error: {
          icon: <XCircle size={20} />,
          style: {
            background: currentColors.background,
            color: currentColors.error,
            border: `1px solid ${currentColors.border}`,
          },
          iconTheme: {
            primary: currentColors.error,
            secondary: currentColors.background,
          },
        },
        loading: {
          icon: <Info size={20} />,
          style: {
            background: currentColors.background,
            color: currentColors.text,
            border: `1px solid ${currentColors.border}`,
          },
          iconTheme: {
            primary: currentColors.info,
            secondary: currentColors.background,
          },
        },
      }}
    />
  );
};
