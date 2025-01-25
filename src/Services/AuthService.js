import $api from "../http";

export default class AuthService{
    static async login(email, password){
        return $api.post('api/login', {email, password})
    }

    static async regist(name, lastName, city, email, password){
        return $api.post('api/register', {name, lastName, city, email, password})
    }

    static async logout(){
        return $api.post('api/logout')
    }
}