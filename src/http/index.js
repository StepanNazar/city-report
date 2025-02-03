import axios from 'axios'
const $api = axios.create({
    withCredentials: true
});

$api.interceptors.request.use((config)=>{
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`
    return config
})

$api.interceptors.request.use((config)=>{
    return config;
}, async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && error.config && !error.config._isRetry) {
        originalRequest._isRetry = true;
        try {
            const response = await axios.get(`api/refresh`, {
                withCredentials: true,
            });
            localStorage.setItem('token', response.data.access_token);

            return $api.request(originalRequest);
        } catch (e) {
            console.log('НЕ АВТОРИЗОВАНИЙ');
        }
    }

    throw error;
});



export default $api