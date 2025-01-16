import React, {useEffect, useState, useRef} from 'react';
import FormButton from './UI/button/button';
import FormInput from './UI/input/FormInput';
const PostForm = function({createPost, ...probs}){
    const [title, setTilte] = useState('');
    const inputRef = useRef();

    const addPost = (e) => {
      e.preventDefault()
      const post = {title: title, body: inputRef.current.value, id: Date.now()%101}
      createPost(post)
      setTilte('');
      inputRef.current.value = '';
    }

    return <form>
        <FormInput
        value={title}
        onChange={event => {setTilte(event.target.value)}}
        type='text' placeholder='title' 
        />
        <FormInput ref={inputRef} type='text' placeholder='description' />
        <FormButton onClick={addPost}>Add post</FormButton>
  </form>
}
export default PostForm