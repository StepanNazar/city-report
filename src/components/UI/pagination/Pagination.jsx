import React, {useState} from 'react';
import { getPagesArray } from '../../../utils/pages';
const Pagination = function({setPage, totalPostPages, page}){
    let pagesArray = getPagesArray(totalPostPages);
    console.log(pagesArray)
    return <div className='page__wrapper'>
    {
      pagesArray.map((p)=>{
        return <span onClick={()=>{setPage(p)}} className={p == page?'page page__current' :'page' } key={p}>{p}</span>
      })
    }
  </div>
}
export default Pagination