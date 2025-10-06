import React from 'react';
import cl from '../newModal/Modal.module.css' 
const ModalAddPost = ({children, visible, setVisible})=>{
    const rootClasses = [cl.modalContainer];
    if(visible) rootClasses.push(cl.active)
    return <div className={rootClasses.join(' ')} onClick={()=>{setVisible(false)}}>
        <div className={cl.modalContent} onClick={(e)=>e.stopPropagation()}>
            {children}
        </div>
    </div>
}
export default ModalAddPost