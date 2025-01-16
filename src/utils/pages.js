export const getPageCount = (totalCount, limit)=>{
    return Math.ceil(totalCount / limit);
}

export const getPagesArray = (totalPostPages)=>{
    let pagesArray = []
    for(let i = 0; i < totalPostPages; i++){
        pagesArray.push(i+1)
    }
    return pagesArray
}