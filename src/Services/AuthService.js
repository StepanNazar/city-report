import $api from "../http";

export default class AuthService{
    static async login(usernsme, password){
        return $api.post('api/login', {usernsme, password})
    }

    static async regist(name, lastName, city, usernsme, password){
        return $api.post('api/register', {name, lastName, city, usernsme, password})
    }

    static async logout(){
        return $api.post('api/logout')
    }
}