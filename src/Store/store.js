import { makeAutoObservable } from "mobx"
import AuthService from "../Services/AuthService";
import { useNavigate } from 'react-router-dom';
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
           const response = await axios.post(`api/login`, {email, password}); 
           localStorage.setItem('token', response.data.accessToken);
            await this.getUserData();
            await this.checkAuth();
        } catch (error) {
            console.log(error.response?.data?.messege)
        }
    }

    async regist(name, lastName, city, email, password){

        try {
           const response = await AuthService.regist(name, lastName, city, email, password); 
           localStorage.setItem('token', response.data.accessToken);
           this.getUserData()
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
    async getUserData(){
        try {
            const response = await AuthService.getUser();
            console.log("Auth Response:", response);
            this.setAuth(true);
            this.setUser(response.data.user); 
        } catch (error) {
            console.log(error);
        }   
    }

    async checkAuth() {
        try {
          const response = await axios.get(`api/refresh`, {
            withCredentials: true,
          });
          localStorage.setItem('token', response.data.accessToken);
          await this.getUserData();
        } catch (e) {
          console.log('НЕ АВТОРИЗОВАНИЙ Користувач: ', e);
          this.setAuth(false);
          localStorage.removeItem('token');
        }
      }
      
      
}