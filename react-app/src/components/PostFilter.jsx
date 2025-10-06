import React, {useEffect, useState, useRef} from 'react';
import FormInput from './UI/input/FormInput';
import PostFilterSelect from './UI/PostFilterSelect/PostFilterSelect';
const PostFiler = function({filter, setFilter}){
    return <div>
        <FormInput placeholder="Serach"
        value={filter.query}
        onChange={(e)=>setFilter({...filter, query: e.target.value})}
        />
        <PostFilterSelect value ={filter.sort} 
        defaultValue="Sort"
        selectOption={selectedOption => {setFilter({...filter, sort: selectedOption})}}
        options={[
        {value: "title", name: "By title"},
        {value: "body", name: "By description"}
        ]}/>
  </div>
}
export default PostFiler