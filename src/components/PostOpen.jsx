import React, {useState} from 'react';
import FormButton from './UI/button/button';
import {useNavigate} from "react-router-dom";
const PostOpen = function(probs){
    let post = probs.post;
    const route = useNavigate();
    return <div className='post'>      
        <div className="post__content">
            <h3>{post.id}. {post.title}</h3>
            <div>
                {post.body}
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