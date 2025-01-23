import axios from 'axios';
export default class PostService{
    static async getAll(limit, page){
            const response = await axios.get('/api/posts', {
                params: {
                    limit: limit,
                    page: page
                }
            });
            return response;
    }
    static async getPost(id){
        const response = await axios.get('/api/postsDetailed', {
            params: {
                id: id
            }
        });
        return response;
    }

    static async getComentsFor(id){
        const response = await axios.get('https://jsonplaceholder.typicode.com/posts/'+id+'/comments', /*{
            params: {
                id: id
            }
        }*/);
        return response;
    }

    static async addPost(post){
        await axios.post('/api/posts', post)
            .then((response) => {       
                console.log(response.data.id, " id - succsessfully added");
            })
            .catch((error)=> {
                // handle error
                console.log(error);
            })
    }

    static async deletePost(post){
        try{
            const response = await axios.delete('/api/posts', {
                data: {data: post}, 
            });
            if (response.status === 200) {
                console.log(`Post with ID ${post.id} was successfully deleted.`);
            }else {
                console.error('Failed to delete post:', response.status, response.statusText);
            }
        }
         catch (error) {
          console.error('Error occurred while deleting post:', error.message);
        }
    }
}