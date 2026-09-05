import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
})

let isRefreshing = false
let refreshSubscribers: ((token: string)=>void)[] = []

function onRefreshed(token: string){
  refreshSubscribers.forEach(cb => cb(token))
  refreshSubscribers = []
}

function addRefreshSubscriber(cb: (token: string)=>void){
  refreshSubscribers.push(cb)
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if(token && config.headers) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(undefined, async (error) => {
  const originalRequest = error.config
  if(error.response && error.response.status === 401 && !originalRequest._retry){
    originalRequest._retry = true
    const refresh = localStorage.getItem('refresh_token')
    if(!refresh) return Promise.reject(error)
    if(isRefreshing){
      return new Promise((resolve) => {
        addRefreshSubscriber((token:string)=>{
          originalRequest.headers['Authorization'] = 'Bearer ' + token
          resolve(api(originalRequest))
        })
      })
    }
    isRefreshing = true
    try{
      const res = await axios.post(`${API_URL}/auth/token/refresh/`, {refresh})
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh || refresh)
      onRefreshed(res.data.access)
      originalRequest.headers['Authorization'] = 'Bearer ' + res.data.access
      return api(originalRequest)
    }catch(err){
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      return Promise.reject(err)
    }finally{
      isRefreshing = false
    }
  }
  return Promise.reject(error)
})

export default api
