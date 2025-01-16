import React, { useRef } from 'react';
import Post from './Post';
import {CSSTransition,TransitionGroup,} from 'react-transition-group';
const PostList = function({posts, title, remove}){
    const nodeRef = useRef(null);
    if(!posts.length){
        return <h2 style={{textAlign: 'center'}}>Empty posts!</h2>
    }
    
    return <div>      
        <h2 style={{textAlign: 'center', marginBottom: '15px'}}>{title}</h2>
        <TransitionGroup>
        {posts.map((post)=>{
            return  <CSSTransition
                nodeRef={nodeRef}
              key={post.id}
              timeout={200}
              classNames="post"
            >
                <Post remove={remove} post={post}/>
            </CSSTransition>
        })}
        </TransitionGroup>
    </div>
}
export default PostList