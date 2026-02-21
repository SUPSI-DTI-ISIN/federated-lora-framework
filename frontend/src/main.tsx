import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import {BrowserRouter} from 'react-router-dom'
import './index.css'
import App from './App.tsx'
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {ReactQueryDevtools} from "@tanstack/react-query-devtools";
import {AuthProviders} from "./providers/auth/AuthProviders.tsx";
import {SelectorRealmProvider} from "./providers/realm/SelectorRealmProvider.tsx";
import {ApiProviders} from "./providers/api/ApiProviders.tsx";

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: 3,
            staleTime: 30_000,
            gcTime: 5 * 60 * 1000,
            refetchOnWindowFocus: true,
            refetchOnReconnect: true,
            refetchOnMount: true,
        }
    }
});

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <QueryClientProvider client={queryClient}>
            <SelectorRealmProvider>
                <AuthProviders>
                    <ApiProviders>
                        <BrowserRouter>
                            <App/>
                            <ReactQueryDevtools initialIsOpen={false}/>
                        </BrowserRouter>
                    </ApiProviders>
                </AuthProviders>
            </SelectorRealmProvider>
        </QueryClientProvider>
    </StrictMode>,
)
