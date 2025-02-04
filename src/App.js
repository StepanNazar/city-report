import { BrowserRouter, Route, Routes, Navigate, useNavigate } from "react-router-dom";
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
import AuthCheck from "./utils/Authcheck";

function App() {
  const { USER } = useContext(UserContext);


  return (
    <BrowserRouter>
      <AuthCheck/>
      <NavBar />
      <Routes> 
        <Route
          path="*"
          element={
            USER.isAuth ? (
              <Routes>
                <Route path="/about" element={<About />} />
                <Route path="/posts" element={<Post />} />
                <Route path="/posts/:id" element={<PostInf />} />
                <Route path="*" element={<Post />} />
              </Routes>
            ) : (
              <Navigate to="/log" replace />
            )
          }
        />
        <Route path="/log" element={<Login />} />
        <Route path="/reg" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

export default observer(App);
