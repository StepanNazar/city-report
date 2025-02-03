import React,  {useContext, useState} from 'react';
import Button from '../components/UI/button/button';
import FormInput from '../components/UI/input/FormInput';
import {useNavigate} from "react-router-dom";
import { UserContext } from '..';
import { observer } from 'mobx-react-lite';

    
const Login = () => {
    const [log, setLogin] = useState('');
    const [password, setPassword] = useState('');
    const route = useNavigate();
    const {USER} = useContext(UserContext)

    
    return <form className='auth_form'>
        <FormInput
            value={log}
            onChange={event => {setLogin(event.target.value)}}
            type='text' placeholder='login' 
        />
        <FormInput
            value={password}
            onChange={event => {setPassword(event.target.value)}}
            type='password' placeholder='password' />
        <div className='auth_btn'>
            <Button onClick={async(e)=>{ e.preventDefault(); await USER.login(log, password)}}>Login</Button>
            <Button onClick={()=>route(`/reg`)}>GO to Registretion</Button>
        </div>
  </form>
};

export default observer(Login);