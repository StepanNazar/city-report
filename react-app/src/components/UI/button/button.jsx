import React from 'react';
import classes from './Button.module.css' 
const Button = function({children, className, ...probs}){
    const combinedClassName = `${classes.button} ${className || ''}`.trim();
    return <button {...probs} className={combinedClassName}>{children}</button>
}
export default Button