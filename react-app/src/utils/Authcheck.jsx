import { useContext, useEffect } from "react";
import { UserContext } from "..";
import { useNavigate } from "react-router-dom";
import { observer } from "mobx-react-lite";

const AuthCheck = observer(() => {
  const { USER } = useContext(UserContext);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      await USER.checkAuth();
      if (USER.isAuth) {
        console.log("move to posts")
        navigate("/posts"); // Перенаправлення після авторизації
      }
    };
    checkAuth();
  }, [USER.isAuth]);

  return null; // Цей компонент не рендерить UI, лише виконує логіку
});

export default AuthCheck;
