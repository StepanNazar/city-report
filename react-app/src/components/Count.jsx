import React, {useState} from 'react';

const Counter = function(){
    const [like, setLike] = useState(0);

    function increment(){
        setLike(like + 1)
      }
      function decrement(){
        setLike(like - 1)
      }

    return <div>      
        <h1>{like}</h1>
      <button onClick={increment}>Like</button>
      <button onClick={decrement}>Dislike</button>
    </div>
}
export default Counter