import React, { useRef } from 'react';

import Coment from '../components/UI/Coment/Coment';
import {CSSTransition,TransitionGroup,} from 'react-transition-group';
const CommentList = function({coments, title, remove}){
    if(!coments.length){
        return <h2 style={{textAlign: 'center'}}>Empty posts!</h2>
    }  
    return <div>      
        <h2 style={{textAlign: 'center', marginBottom: '15px'}}>{title}</h2>
        <div>
            {coments.map((c)=>{
            return  <Coment com={c} key={c.id}/>
            })}
            </div>
    </div>
}
export default CommentList