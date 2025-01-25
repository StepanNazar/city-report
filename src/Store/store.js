import { makeAutoObservable } from "mobx"
import AuthService from "../Services/AuthService";
import axios from 'axios'
export default class USER_INFO{
    user = {}
    isAuth = false;
    constructor(){
        makeAutoObservable(this)
    }

    setAuth(bool){
        this.isAuth = bool;
    }

    setUser(user){
        this.user = user;
    }

    async login(email, password){
        try {
           const response = await AuthService.login(email, password); 
           localStorage.setItem('token', response.data.accessToken);
           this.setAuth(true);
           this.setUser(response.data.user)
        } catch (error) {
            console.log(error.response?.data?.messege)
        }
    }

    async regist(name, lastName, city, email, password){
        try {
           const response = await AuthService.regist(name, lastName, city, email, password); 
           localStorage.setItem('token', response.data.accessToken);
           this.setAuth(true);
           this.setUser(response.data.user)
        } catch (error) {
            console.log(error.response?.data?.messege)
        }
    }

    async logout(email, password){
        try {
           const response = await AuthService.logout(); 
           localStorage.removeItem('token');
           this.setAuth(false);
           this.setUser({});
        } catch (error) {
            console.log(error.response?.data?.messege)
        }
    }

    async checkAuth() {
        try {
          const response = await axios.get(`api/refresh`, {
            withCredentials: true,
          });
      
          console.log("Auth Response:", response);
      
          // Зберігаємо токен у LocalStorage
          localStorage.setItem("token", response.data.accessToken);
      
          // Оновлюємо стан автентифікації та користувача
          this.setAuth(true);
          this.setUser(response.data.user);
        } catch (error) {
          console.error("Authentication failed:", error?.response?.data?.message || error.message);
        }
      }
      
}