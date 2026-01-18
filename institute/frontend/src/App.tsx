import {Toaster} from "react-hot-toast";
import './App.css'
import {Route, Routes} from "react-router-dom";
import { Home } from "./pages/Home";
import { DocumentsPage } from "./pages/DocumentsPage";
import { ChatPage } from "./pages/ChatPage";
import {Header} from "./components/common/Header.tsx";
import {Footer} from "./components/common/Footer.tsx";

const App = () => {
    return (
        <div className="min-h-screen flex flex-col bg-base-100">
            <Toaster
                position="bottom-right"
                toastOptions={{
                    className: 'bg-base-200 text-base-content',
                    duration: 4000,
                }}
            />
            <Header />
            <main className="flex-1">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/documents" element={<DocumentsPage/>}/>
                    <Route path="/chat" element={<ChatPage/>}/>
                </Routes>
            </main>
            <Footer />
        </div>
    )
}

export default App