import React from 'react';
import classes from './Input.module.css' 
const FormInput = React.forwardRef((probs, ref)=>{
    return <input ref={ref} {...probs} className={classes.input} />
})
export default FormInput