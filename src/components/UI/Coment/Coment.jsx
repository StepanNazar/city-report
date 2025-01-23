import React, {useState} from 'react';
import FormButton from '../button/button';
import {useNavigate} from "react-router-dom";
const PostOpen = function(probs){
    
    let com = probs.com;
    return <div className='post'>      
        <div className="post__content">
            <h3>{com.name}</h3>
            <div>
                {com.body}
            </div>
        </div> 

        {/*
        <div className="post__btn">

            <FormButton onClick={()=>route(`/posts/${post.id}`)} className="about_post">Розгорнути</FormButton>
            <FormButton onClick={()=>probs.remove(post)}>Виконано</FormButton>
        </div>*/}
    </div>
}
export default PostOpen