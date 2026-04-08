import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, useNavigate } from 'react-router-dom'
import { ClerkProvider } from '@clerk/clerk-react'
import App from './App.tsx'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
})

// eslint-disable-next-line react-refresh/only-export-components
function ClerkProviderWithNavigate({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate()
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const clerkPubKey = (import.meta as any).env.VITE_CLERK_PUBLISHABLE_KEY

  if (!clerkPubKey) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          fontFamily: 'Inter, system-ui, sans-serif',
          background: '#0b0f19',
          color: '#e6edf3',
        }}
      >
        <div style={{ maxWidth: '720px', lineHeight: 1.6 }}>
          <h1 style={{ fontSize: '22px', marginBottom: '10px' }}>Missing environment variable</h1>
          <p style={{ marginBottom: '8px' }}>
            <code>VITE_CLERK_PUBLISHABLE_KEY</code> is not set, so authentication cannot initialize.
          </p>
          <p style={{ marginBottom: '8px' }}>
            Create <code>Frontend/.env</code> and add:
          </p>
          <pre style={{ background: '#111827', padding: '12px', borderRadius: '8px' }}>
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxx_or_pk_live_xxx
          </pre>
          <p>Then restart the frontend dev server.</p>
        </div>
      </div>
    )
  }

  return (
    <ClerkProvider
      publishableKey={clerkPubKey}
      routerPush={(to: string) => navigate(to)}
      routerReplace={(to: string) => navigate(to, { replace: true })}
      signInFallbackRedirectUrl="/dashboard"
      signUpFallbackRedirectUrl="/dashboard"
    >
      {children}
    </ClerkProvider>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ClerkProviderWithNavigate>
          <App />
        </ClerkProviderWithNavigate>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
