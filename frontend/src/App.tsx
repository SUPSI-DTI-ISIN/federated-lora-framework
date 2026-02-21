import {Toaster} from "react-hot-toast";
import './App.css'
import {Outlet, Route, Routes} from "react-router-dom";
import {Home} from "./pages/Home";
import {DocumentsPage} from "./pages/DocumentsPage";
import {ChatPage} from "./pages/ChatPage";
import {Header} from "./components/common/Header.tsx";
import {Footer} from "./components/common/Footer.tsx";
import {AdaptersPage} from "./pages/AdaptersPage.tsx";
import {SectionsPage} from "./pages/SectionsPage.tsx";
import {ProtectedRoute} from "./routes/ProtectedRoute.tsx";
import {RealmsPage} from "./pages/RealmsPage.tsx";
import {RealmsAdminPage} from "./pages/RealmsAdminPage.tsx";
import {AdaptersAdminPage} from "./pages/AdaptersAdminPage.tsx";

const App = () => {
    return (
        <>
            <Toaster
                position="bottom-right"
                toastOptions={{
                    className: 'bg-base-200 text-base-content',
                    duration: 4000,
                }}
            />
            <Header/>
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
            </Routes>
            <Footer/>
        </>
    )
}

export default App