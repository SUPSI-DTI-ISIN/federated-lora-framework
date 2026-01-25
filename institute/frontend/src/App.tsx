import {Toaster} from "react-hot-toast";
import './App.css'
import {Route, Routes} from "react-router-dom";
import {Home} from "./pages/Home";
import {DocumentsPage} from "./pages/DocumentsPage";
import {ChatPage} from "./pages/ChatPage";
import {Header} from "./components/common/Header.tsx";
import {Footer} from "./components/common/Footer.tsx";
import {AdaptersPage} from "./pages/AdaptersPage.tsx";

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
                <Route path="/" element={<Home/>}/>
                <Route path="/documents" element={<DocumentsPage/>}/>
                <Route path="/chat" element={<ChatPage/>}/>
                <Route path="/adapters" element={<AdaptersPage/>}/>
            </Routes>
            <Footer/>
        </>
    )
}

export default App