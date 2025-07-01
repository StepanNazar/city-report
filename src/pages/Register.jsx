import React, {useContext, useState} from 'react';
import Button from '../components/UI/button/button';
import FormInput from '../components/UI/input/FormInput';
import {useNavigate} from "react-router-dom";
import { UserContext } from '..';
import { observer } from 'mobx-react-lite';


const Register = () => {
    const [name, setName] = useState('');
    const [lastName, setLastName] = useState('');
    const [city, setCity] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const {USER} = useContext(UserContext)
    const route = useNavigate();
    
    return <form className='auth_form'>
        <FormInput
            value={name}
            onChange={event => {setName(event.target.value)}}
            type='text' placeholder='Your name' 
        />
        <FormInput
            value={lastName}
            onChange={event => {setLastName(event.target.value)}}
            type='text' placeholder='Your last name' 
        />
        <FormInput
            value={city}
            onChange={event => {setCity(event.target.value)}}
            type='text' placeholder='City to observe' 
        />
        <FormInput
            value={email}
            onChange={event => {setEmail(event.target.value)}}
            type='text' placeholder='email' 
        />
        <FormInput
            value={password}
            onChange={event => {setPassword(event.target.value)}}
            type='password' placeholder='Password' />
        <div className='auth_btn'>
            <Button onClick={async(e)=>{e.preventDefault(); await USER.regist(name, lastName, city, email, password); route('/post')}}>Register</Button>
            <Button onClick={()=>route(`/log`)}>Go to Login</Button>
        </div>
  </form>
};

export default observer(Register);