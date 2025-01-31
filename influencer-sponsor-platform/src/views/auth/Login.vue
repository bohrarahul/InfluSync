<template>
  <div class="login-container">
    <!-- Animated background circles -->
    <div class="login-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="login-card">
      <div class="login-header">
        <h2>Welcome Back</h2>
        <p>Sign in to continue to your dashboard</p>
      </div>

      <transition name="fade">
        <div v-if="error" class="error-message" key="error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
            <path d="M12 8v5M12 16h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ error }}
        </div>
      </transition>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2M12 11a4 4 0 100-8 4 4 0 000 8z"/>
            </svg>
            <input 
              id="username"
              type="text" 
              v-model="form.username" 
              required 
              placeholder="Enter your username"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0110 0v4"/>
            </svg>
            <input 
              id="password"
              type="password" 
              v-model="form.password" 
              required 
              placeholder="Enter your password"
            >
          </div>
          <router-link to="/forgot-password" class="forgot-password">
            Forgot Password?
          </router-link>
        </div>

        <button 
          type="submit" 
          class="btn-login" 
          :disabled="isLoading"
        >
          <span v-if="isLoading">
            <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
            </svg>
            Logging in...
          </span>
          <span v-else>Login</span>
          <span class="shine"></span>
        </button>
      </form>

      <div class="register-link">
        Don't have an account? 
        <router-link to="/register">Register here</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      error: null,
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      this.error = null
      
      if (!this.form.username || !this.form.password) {
        this.error = 'Please enter both username and password'
        return
      }

      this.isLoading = true

      try {
        const response = await axios.post('/login', this.form)
        
        localStorage.setItem('token', response.data.access_token)
        localStorage.setItem('username', response.data.username)
        localStorage.setItem('userRole', response.data.role.toLowerCase())

        const roleRoutes = {
          'admin': '/admin/dashboard',
          'sponsor': '/sponsor/dashboard',
          'influencer': '/influencer/dashboard'
        }

        const redirectRoute = roleRoutes[response.data.role.toLowerCase()] || '/'
        this.$router.push(redirectRoute)

      } catch (err) {
        if (err.response) {
          switch (err.response.status) {
            case 403:
              this.error = 'Account not yet approved'
              break
            case 401:
              this.error = 'Invalid username or password'
              break
            default:
              this.error = 'An unexpected error occurred'
          }
        } else {
          this.error = 'Network error. Please check your connection'
        }
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.circle {
  position: absolute;
  border-radius: 50%;
  opacity: 0.15;
}

.circle-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
  top: -100px;
  left: -100px;
  animation: float 20s infinite;
}

.circle-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
  top: 40%;
  right: -200px;
  animation: float 25s infinite reverse;
}

.circle-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
  bottom: -50px;
  left: 50%;
  animation: float 15s infinite;
}

@keyframes float {
  0% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(30px, -30px) rotate(120deg); }
  66% { transform: translate(-20px, 20px) rotate(240deg); }
  100% { transform: translate(0, 0) rotate(360deg); }
}

.login-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 100%;
  max-width: 450px;
  padding: 2.5rem;
  position: relative;
  z-index: 2;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.login-card:hover {
  transform: translateY(-5px);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.login-header p {
  color: #94a3b8;
  font-size: 1rem;
}

.error-message {
  background: rgba(220, 38, 38, 0.1);
  color: #ef4444;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  border: 1px solid rgba(220, 38, 38, 0.2);
}

.error-icon {
  width: 20px;
  height: 20px;
  margin-right: 0.75rem;
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #94a3b8;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #6366f1;
}

input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.08);
}

input::placeholder {
  color: #64748b;
}

.forgot-password {
  position: absolute;
  right: 0;
  top: 0;
  color: #60a5fa;
  font-size: 0.875rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #93c5fd;
}

.btn-login {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
}

.btn-login:hover {
  transform: translateY(-2px);
}

.btn-login:disabled {
  background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
  cursor: not-allowed;
}

.shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shine 3s infinite;
}

@keyframes shine {
  100% {
    left: 100%;
  }
}

.spinner {
  animation: spin 1s linear infinite;
  width: 20px;
  height: 20px;
  display: inline-block;
  vertical-align: middle;
  margin-right: 0.5rem;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #94a3b8;
}

.register-link a {
  color: #60a5fa;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.register-link a:hover {
  color: #93c5fd;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 640px) {
  .login-card {
    padding: 2rem;
  }

  .login-header h2 {
    font-size: 1.75rem;
  }

  .forgot-password {
    position: relative;
    display: block;
    text-align: right;
    margin-top: 0.5rem;
  }
}
</style>