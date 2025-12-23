import {Toaster} from "react-hot-toast";
import './App.css'
import {Route, Routes} from "react-router-dom";
import { Home } from "./pages/Home";
import {Header} from "./components/common/Header.tsx";
import {Footer} from "./components/common/Footer.tsx";


const App = () => {
    return (
        <>
            <Toaster position="bottom-right"/>
            <Header />
            <Routes>
                <Route path="/" element={<Home/>}/>
            </Routes>
            <Footer />
        </>
    )
}

export default App
