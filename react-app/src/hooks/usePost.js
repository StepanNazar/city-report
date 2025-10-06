import  {useMemo} from 'react';
export const useSortedPosts = (posts, sort)=>{
    const getSortedPost = ()=>{
        if(!sort) return posts;
        return [...posts].sort((a,b)=>{return a[sort].localeCompare(b[sort])});
    }

    return useMemo(getSortedPost, [sort, posts])
}
export const useSearchedPosts = (posts, sort, query)=>{
  const sortedPost = useSortedPosts(posts, sort);
  const sortedAndSearchPost = useMemo(()=>{
    return sortedPost.filter((post)=>{return post.title.toLowerCase().includes(query)})
  }, [query, sortedPost])
  return sortedAndSearchPost;
}