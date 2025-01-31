<template>
  <div class="register-container">
    <!-- Animated background circles -->
    <div class="register-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="register-card">
      <div class="register-header">
        <h2>Create Your Account</h2>
        <p>Join the Influencer-Sponsor Platform</p>
      </div>

      <transition name="fade">
        <div v-if="error" class="error-message" key="error">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
            <path d="M12 8v5M12 16h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ error }}
        </div>
      </transition>

      <form @submit.prevent="handleRegister" class="register-form">
        <!-- Username Field -->
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
              placeholder="Choose a unique username"
              minlength="3"
              maxlength="20"
            >
          </div>
        </div>

        <!-- Email Field -->
        <div class="form-group">
          <label for="email">Email</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            <input 
              id="email"
              type="email" 
              v-model="form.email" 
              required 
              placeholder="Enter your email address"
            >
          </div>
        </div>

        <!-- Password Field -->
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
              placeholder="Create a strong password"
              minlength="8"
            >
          </div>
          <p class="password-hint">
            Password must be at least 8 characters long
          </p>
        </div>

        <!-- Role Selection -->
        <div class="form-group">
          <label for="role">Account Type</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M9 11a4 4 0 100-8 4 4 0 000 8zM23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/>
            </svg>
            <select 
              id="role"
              v-model="form.role" 
              required
              class="custom-select"
            >
              <option value="influencer">Influencer</option>
              <option value="sponsor">Sponsor</option>
            </select>
          </div>
        </div>

        <!-- Sponsor Notice -->
        <transition name="slide">
          <div 
            v-if="form.role === 'sponsor'" 
            class="sponsor-notice"
            key="sponsor-notice"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="notice-icon">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 8v4M12 16h.01"/>
            </svg>
            <p>
              Sponsor accounts require admin approval before login. 
              Verification may take 1-2 business days.
            </p>
          </div>
        </transition>

        <!-- Submit Button -->
        <button 
          type="submit" 
          class="btn-register"
          :disabled="isLoading"
        >
          <span v-if="isLoading">
            <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
            </svg>
            Creating Account...
          </span>
          <span v-else>Register</span>
          <span class="shine"></span>
        </button>
      </form>

      <div class="login-link">
        Already have an account? 
        <router-link to="/login">Login here</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        role: 'influencer'
      },
      error: null,
      isLoading: false
    }
  },
  methods: {
    async handleRegister() {
      this.error = null
      
      if (this.form.password.length < 8) {
        this.error = 'Password must be at least 8 characters long'
        return
      }

      this.isLoading = true

      try {
        const response = await axios.post('/register', this.form)
        
        if (response.status === 201) {
          if (this.form.role === 'sponsor') {
            this.$router.push({
              path: '/login',
              query: { 
                message: 'Registration successful. Please wait for admin approval.',
                type: 'success'
              }
            })
          } else {
            this.$router.push({
              path: '/login',
              query: { 
                message: 'Account created successfully. Please log in.',
                type: 'success'
              }
            })
          }
        }
      } catch (err) {
        if (err.response && err.response.data) {
          this.error = err.response.data.message || 'Registration failed'
        } else {
          this.error = 'Network error. Please check your connection.'
        }
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>
<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
}

.register-bg {
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

.register-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 100%;
  max-width: 500px;
  padding: 2.5rem;
  position: relative;
  z-index: 2;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.register-card:hover {
  transform: translateY(-5px);
}

.register-header {
  text-align: center;
  margin-bottom: 2rem;
}

.register-header h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-header p {
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

input, .custom-select {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus, .custom-select:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.08);
}

input::placeholder {
  color: #64748b;
}

.custom-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236366f1'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'%3E%3C/path%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.5em;
  padding-right: 2.5rem;
}

.custom-select option {
  background-color: #1e1b4b;
  color: white;
}

.password-hint {
  color: #94a3b8;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.sponsor-notice {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.2);
  color: #818cf8;
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.notice-icon {
  width: 20px;
  height: 20px;
  margin-right: 0.75rem;
  color: #818cf8;
}

.btn-register {
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

.btn-register:hover {
  transform: translateY(-2px);
}

.btn-register:disabled {
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

.login-link {
  text-align: center;
  margin-top: 1.5rem;
  color: #94a3b8;
}

.login-link a {
  color: #60a5fa;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.login-link a:hover {
  color: #93c5fd;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 640px) {
  .register-card {
    padding: 2rem;
  }

  .register-header h2 {
    font-size: 1.75rem;
  }

  .form-group {
    margin-bottom: 1.25rem;
  }

  input, .custom-select {
    padding: 0.75rem 1rem 0.75rem 2.75rem;
  }

  .input-icon {
    width: 18px;
    height: 18px;
  }

  .sponsor-notice {
    padding: 0.875rem;
  }

  .btn-register {
    padding: 0.875rem;
  }
}

@media (max-width: 380px) {
  .register-card {
    padding: 1.5rem;
  }

  .register-header h2 {
    font-size: 1.5rem;
  }

  .register-header p {
    font-size: 0.875rem;
  }

  .password-hint {
    font-size: 0.75rem;
  }
}
</style>