import React from 'react';
import classes from './Button.module.css' 
const Button = function({children, ...probs}){
    return <button {...probs} className={classes.button}>{children}</button>
}
export default Button