import React, {useEffect, useState} from 'react';
import { useParams } from 'react-router-dom';
import {useNavigate} from "react-router-dom";
import FormButton from '../components/UI/button/button';
import { useFetching } from '../hooks/useFetching';
import PostService from '../components/API/PostService';
import PostOpen from '../components/PostOpen';
import Loader from '../components/UI/Loader/Loader';
import CommentList from '../components/CommentList';
const PostInf = () => {
    const params = useParams()
    const route = useNavigate();
    const id = params.id;
    const[post, setPost] = useState({})
    const[coments, setComents] = useState([])
    const [fetchPost,isPostLoading, postError] = useFetching(async()=>{
          const response = await PostService.getPost(id);      
          //console.log(response)
          setPost(response.data);
    })
    const [fetchComents,isComLoading, comError] = useFetching(async()=>{
        const response = await PostService.getComentsFor(id);      
        //console.log(response.data)
        setComents(response.data);

    })
      useEffect(()=>{
        fetchPost();
      }, [])
      useEffect(()=>{
        fetchComents();
      }, [])
  return (
    <div>
         <FormButton onClick={()=>route(-1)} className="about_post">Назад</FormButton>
     {
        isPostLoading || isComLoading
        ?<div style={{display: 'flex', justifyContent: 'center', marginTop: '50px'}}><Loader/></div>
        :<div>
            <PostOpen post={post}/>
            <CommentList coments={coments} title={"Comments"}/>
        </div>
      }
    
    </div>
  );
};

export default PostInf;