import  {useMemo} from 'react';
export const addPost = (setPost, setModal, posts)=>{
    return (newpost)=>{
        setPost([...posts, newpost]);
        setModal(false)
    }   
}