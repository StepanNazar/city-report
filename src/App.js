import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import Post from "./pages/Post";
import './styles/app.css';
import About from "./pages/About";
import NavBar from "./components/UI/navbar/NavBar";
import PostInf from "./pages/PostInf";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { useContext, useEffect } from "react";
import React from "react";
import { UserContext } from ".";
import { observer } from "mobx-react-lite";

function App() {
  const { USER } = useContext(UserContext);

  useEffect(() => {
    USER.checkAuth(); // Виклик перевірки автентифікації при завантаженні
  }, []);

  return (
    <BrowserRouter>
      <NavBar />
      <Routes> 
        {/* Захищений маршрут для незареєстрованих користувачів */}
        <Route
          path="*"
          element={
            USER.iaAuth ? (
              <Routes>
                <Route path="/about" element={<About />} />
                <Route path="/posts" element={<Post />} />
                <Route path="/posts/:id" element={<PostInf />} />
                <Route path="*" element={<Post />} />
              </Routes>
            ) : (
              <Navigate to="/reg" replace />
            )
          }
        />
        {/* Вільний доступ до сторінок авторизації */}
        <Route path="/log" element={<Login />} />
        <Route path="/reg" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default observer(App);
