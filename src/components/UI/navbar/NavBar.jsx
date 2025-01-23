import React, { useContext } from 'react';
import {Link} from "react-router-dom";
import { UserContext } from '../../..';
import { observer } from 'mobx-react-lite';
const NavBar = () => {
  const {USER} = useContext(UserContext)
  const logout = async()=>{
    USER.logout();
  }
  return (
    <div className="navbar">
      {USER.isAuth? <div className="navbar__linkers">     
      <Link to="/about">About</Link>
      <Link to="/posts">Posts</Link>
      <Link onClick={logout} to="/log">Logout</Link></div>
      :null
      }
    
  </div>
  );
};

export default observer(NavBar);