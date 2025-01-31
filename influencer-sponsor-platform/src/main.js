import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// Set base URL for API requests
axios.defaults.baseURL = 'http://localhost:5000'

// Add JWT token to requests if it exists
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  console.log('Token in interceptor:', token) // Add this log
  
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')