import React, {useEffect, useState, useRef, useMemo} from 'react';
import '../styles/app.css'
import PostList from '../components/PostList';
import PostForm from '../components/PostForm';
import PostFilter from '../components/PostFilter';
import ModalAddPost from '../components/UI/ModalAddPost/ModalAddPost';
import Button from '../components/UI/button/button';
import { useSearchedPosts } from '../hooks/usePost';
import { addPost } from '../hooks/usePostMang';
import { useFetching } from '../hooks/useFetching';
import PostService from '../components/API/PostService';
import Loader from '../components/UI/Loader/Loader';
import { getPageCount } from '../utils/pages';
import Pagination from '../components/UI/pagination/Pagination';

function Post() {
  const[posts, setPost] = useState([])
  const [filter, setFilter]= useState({sort: "", query: ""})
  const [modal, setModal] = useState(false)
  const sortedAndSearchPost = useSearchedPosts(posts, filter.sort, filter.query)
  const clSetpost = addPost(setPost, setModal, posts);
  const[limit, setLimit] = useState(10);
  const[page, setPage] = useState(1);
  const[totalPostPages, setTotalPostPages] = useState(0);

 

  const [fetchPost,isPostLoading, postError] = useFetching(async()=>{
    /*
      const response = await PostService.getAll(limit, page);      
      const test = (response.headers['x-total-count']);
      setTotalPostPages(getPageCount(test, limit));*/
      fetch('http://127.0.0.1:5000/posts').then(res => res.json()).then(data => {
        setPost(data);
      });
    })

  const clRemovepost = (post)=>{
    setPost(posts.filter((p) => p.id !== post.id))
  }
 
 
  useEffect(()=>{
    fetchPost();
  }, [])
  
  useEffect(()=>{
    fetchPost();
  }, [page])

  return (
    <div className="App">
      <Button style={{marginTop: '30px'}} onClick={()=>{setModal(true)}}>Add Post</Button>
      <ModalAddPost visible={modal} setVisible={setModal}>
         <PostForm createPost={clSetpost} />
      </ModalAddPost> 
      <hr style={{margin: '15px 0'}}/>
      <PostFilter filter={filter} setFilter={setFilter}/>
      {postError &&
        <h1>trouble ${postError}</h1>
      }
      {
        isPostLoading
        ?<div style={{display: 'flex', justifyContent: 'center', marginTop: '50px'}}><Loader/></div>
        :<PostList remove={clRemovepost} posts={sortedAndSearchPost} title={"Post list"}/>
      }
      <Pagination setPage={setPage} totalPostPages={totalPostPages} page={page}/>
      
    </div>
  );
}

export default Post;
