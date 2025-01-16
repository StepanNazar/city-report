import React, {useState} from 'react';
import FormButton from './UI/button/button';
const Post = function(probs){
    let post = probs.post;
    return <div className='post'>      
        <div className="post__content">
            <h3>{post.id}. {post.title}</h3>
            <div>
                {post.body}
            </div>
        </div> 
        <div className="post__btn">
            <FormButton onClick={()=>probs.remove(post)}>Delete</FormButton>
        </div>
    </div>
}
export default Post