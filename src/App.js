import { BrowserRouter, Link, Route, Routes} from "react-router-dom";
import Post from "./pages/Post";
import './styles/app.css'
import About from "./pages/About";
import NavBar from "./components/UI/navbar/NavBar";
function App() {
  
  return (
      <BrowserRouter>
        <NavBar></NavBar>
          <Routes>
            <Route path="/about" element={<About />} />
            <Route path="/posts" element={<Post />} />
            <Route path="*" element={<Post />} />
          </Routes> 
      </BrowserRouter>    
  );
}

export default App;
