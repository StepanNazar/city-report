import { makeAutoObservable, toJS } from "mobx"
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

    setUser(userd){
        this.user = { ...userd };
        console.log(toJS(this.user))
        console.log(this.user.name)
    }

    async login(email, password){
        try {
           const response = await axios.post(`api/login`, {email, password}); 
           
           localStorage.setItem('token', response.data.access_token);
           console.log(`Bearer ${localStorage.getItem('token')}`)
            await this.getUserData();
            return 200;
        } catch (error) {
            console.log(error.response?.data?.messege)
        }
    }

    async regist(name, lastName, city, email, password){

        try {
           const response = await AuthService.regist(name, lastName, city, email, password); 
           localStorage.setItem('token', response.data.accessToken);
           console.log(response)
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
            await this.setAuth(true);
            await this.setUser(response.data); 

        } catch (error) {
            console.log(error);
        }   
    }

    async checkAuth() {
        try {
          const response = await axios.get(`api/refresh`, {
            withCredentials: true,
          });
          localStorage.setItem('token', response.data.access_token);
          await this.getUserData();
        } catch (e) {
          console.log('НЕ АВТОРИЗОВАНИЙ Користувач: ', e);
        }
      }
      
      
}