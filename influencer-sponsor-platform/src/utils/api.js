// src/utils/api.js
import axios from 'axios'

export const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL
})

api.interceptors.request.use(config => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})