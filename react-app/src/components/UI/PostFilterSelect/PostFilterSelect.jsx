import React, {useState} from 'react';

const PostFilterSelect = function({options, defaultValue, value, selectOption}){

    return <select value={value}
       onChange={(e)=>{selectOption(e.target.value)}}>      
       <option disabled value="">{defaultValue}</option>
       {options.map((opt)=>{
            return <option value={opt.value} key={opt.value}>{opt.name}</option>
       })}
    </select>
}
export default PostFilterSelect