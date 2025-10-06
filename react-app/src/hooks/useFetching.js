import  {useState} from 'react';
export const useFetching = (callback)=>{
    const [isPostLoading, setIsPostLoading] = useState(false)
    const [error, setError] = useState("")

    const fetching = async()=>{
        try {
            console.log("start")
            setIsPostLoading(true);
            await callback();
        } catch (error) {
            setError(error.message)
        }finally{
            setIsPostLoading(false)
            console.log("end")
        }
    }
    return [fetching, isPostLoading, error];
}