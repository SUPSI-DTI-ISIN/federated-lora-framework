import './App.css'
import {Outlet, Route, Routes} from "react-router-dom";
import {Home} from "./pages/Home";
import {DocumentsPage} from "./pages/DocumentsPage";
import {ChatPage} from "./pages/ChatPage";
import {AdaptersPage} from "./pages/AdaptersPage.tsx";
import {SectionsPage} from "./pages/SectionsPage.tsx";
import {ProtectedRoute} from "./routes/ProtectedRoute.tsx";
import {RealmsPage} from "./pages/RealmsPage.tsx";
import {RealmsAdminPage} from "./pages/RealmsAdminPage.tsx";
import {AdaptersAdminPage} from "./pages/AdaptersAdminPage.tsx";
import {FederatedLearningJobsPage} from "./pages/FederatedLearningJobsPage.tsx";
import {Header} from "./components/common/header/Header.tsx";
import {ThemedToaster} from "./components/common/ThemedToaster.tsx";
import {Footer} from "./components/common/Footer.tsx";
import {ApiProviders} from "./providers/api/ApiProviders.tsx";
import {AuthProviders} from "./providers/auth/AuthProviders.tsx";
import {SelectorRealmProvider} from "./providers/realm/SelectorRealmProvider.tsx";

const App = () => {
    return (
        <SelectorRealmProvider>
            <AuthProviders>
                <ApiProviders>
                    <div className="flex flex-col min-h-screen">
                        <ThemedToaster/>
                        <Header/>
                        <main className="flex-1 w-full">
                            <Routes>
                                <Route
                                    path="/"
                                    element={
                                        <Home/>
                                    }
                                />

                                <Route
                                    path="/realms"
                                    element={
                                        <RealmsPage/>
                                    }
                                />

                                <Route
                                    path="/realms-admin"
                                    element={
                                        <ProtectedRoute departmentAdminOnly={true}>
                                            <RealmsAdminPage/>
                                        </ProtectedRoute>
                                    }
                                />

                                <Route
                                    path="/documents"
                                    element={
                                        <ProtectedRoute>
                                            <Outlet/>
                                        </ProtectedRoute>
                                    }
                                >
                                    <Route index element={<DocumentsPage/>}/>
                                    <Route path=":documentId/sections" element={<SectionsPage/>}/>
                                </Route>

                                <Route
                                    path="/chat"
                                    element={
                                        <ProtectedRoute>
                                            <ChatPage/>
                                        </ProtectedRoute>
                                    }
                                />

                                <Route
                                    path="/adapters"
                                    element={
                                        <ProtectedRoute>
                                            <AdaptersPage/>
                                        </ProtectedRoute>
                                    }
                                />

                                <Route
                                    path="/adapters-admin"
                                    element={
                                        <ProtectedRoute departmentAdminOnly={true}>
                                            <AdaptersAdminPage/>
                                        </ProtectedRoute>
                                    }
                                />

                                <Route
                                    path="/federated-learning-jobs"
                                    element={
                                        <ProtectedRoute departmentAdminOnly={true}>
                                            <FederatedLearningJobsPage/>
                                        </ProtectedRoute>
                                    }
                                />
                            </Routes>
                        </main>
                        <Footer/>
                    </div>
                </ApiProviders>
            </AuthProviders>
        </SelectorRealmProvider>
    )
}

export default App