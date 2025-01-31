<template>
  <div class="profile-management">
    <!-- Background Elements -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="dashboard-content">
      <div class="dashboard-header">
        <h1>Profile Management</h1>
        <p class="header-subtitle">Manage your professional presence</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
        </svg>
        Loading your profile...
      </div>

      <!-- Error State -->
      <div v-if="error" class="error-message">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        {{ error }}
      </div>

      <!-- Profile Form -->
      <form v-if="!loading" class="profile-form" @submit.prevent="saveProfile">
        <!-- Basic Information -->
        <div class="dashboard-section form-section">
          <div class="section-header">
            <h2>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Basic Information
            </h2>
          </div>

          <div class="form-group">
            <label>Full Name</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <input 
                v-model="profile.name"
                type="text"
                required
                placeholder="Your full name"
              >
            </div>
          </div>

          <div class="form-group">
            <label>Bio</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>
              </svg>
              <textarea 
                v-model="profile.bio"
                rows="4"
                placeholder="Tell brands about yourself..."
              ></textarea>
            </div>
          </div>
        </div>

        <!-- Professional Details -->
        <div class="dashboard-section form-section">
          <div class="section-header">
            <h2>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              Professional Details
            </h2>
          </div>

          <div class="form-group">
            <label>Category</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
              </svg>
              <select v-model="profile.category" required>
                <option value="">Select a category</option>
                <option v-for="category in categories" 
                        :key="category" 
                        :value="category">
                  {{ category }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Niche</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
              <select v-model="profile.niche" required>
                <option value="">Select a niche</option>
                <option v-for="niche in getNichesByCategory" 
                        :key="niche" 
                        :value="niche">
                  {{ niche }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Total Reach</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <input 
                v-model.number="profile.reach"
                type="number"
                required
                placeholder="Your total followers/subscribers"
              >
            </div>
          </div>
        </div>

        <!-- Form Actions -->
        <div class="form-actions">
          <button 
            type="submit"
            :disabled="saving || !isFormValid"
            class="action-btn save-btn"
          >
            <svg v-if="!saving" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 13l4 4L19 7"/>
            </svg>
            <svg v-else class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
            </svg>
            {{ saving ? 'Saving Changes...' : 'Save Changes' }}
          </button>
        </div>

        <!-- Completion Warning -->
        <div v-if="!isProfileComplete" class="dashboard-section completion-warning">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <p>Please complete all required fields to be visible to sponsors</p>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ProfileManagement',
  data() {
    return {
      profile: {
        name: '',
        category: '',
        niche: '',
        reach: null,
        bio: ''
      },
      loading: true,
      saving: false,
      error: null,
      categories: [
        'Fashion',
        'Technology',
        'Food',
        'Travel',
        'Lifestyle',
        'Beauty',
        'Gaming',
        'Fitness',
        'Education'
      ],
      nichesByCategory: {
        'Fashion': ['Street Style', 'Luxury Fashion', 'Sustainable Fashion', 'Fashion Tips'],
        'Technology': ['Tech Reviews', 'Programming', 'Gadgets', 'Tech News'],
        'Food': ['Cooking', 'Restaurant Reviews', 'Healthy Eating', 'Baking'],
        'Travel': ['Adventure', 'Budget Travel', 'Luxury Travel', 'Local Guides'],
        'Lifestyle': ['Daily Vlogs', 'Minimalism', 'Productivity', 'Self-improvement'],
        'Beauty': ['Makeup', 'Skincare', 'Hair Care', 'Beauty Reviews'],
        'Gaming': ['Game Reviews', 'Streaming', 'ESports', 'Gaming Tips'],
        'Fitness': ['Workouts', 'Nutrition', 'Weight Training', 'Yoga'],
        'Education': ['Study Tips', 'Online Courses', 'Language Learning', 'Career Advice']
      }
    }
  },
  computed: {
    isFormValid() {
      return this.profile.name && 
             this.profile.category && 
             this.profile.niche && 
             this.profile.reach
    },
    isProfileComplete() {
      return this.isFormValid
    },
    getNichesByCategory() {
      return this.nichesByCategory[this.profile.category] || []
    }
  },
  watch: {
    'profile.category'(newCategory) {
      // Reset niche when category changes
      this.profile.niche = ''
    }
  },
  created() {
    this.fetchProfile()
  },
  methods: {
    async fetchProfile() {
      try {
        this.loading = true
        const response = await axios.get('/profile')
        this.profile = response.data
        this.error = null
      } catch (err) {
        console.error('Error fetching profile:', err)
        this.error = 'Failed to load profile'
      } finally {
        this.loading = false
      }
    },
    async saveProfile() {
      if (!this.isFormValid) return

      try {
        this.saving = true
        await axios.put('/profile', this.profile)
        alert('Profile updated successfully!')
      } catch (err) {
        console.error('Error saving profile:', err)
        this.error = 'Failed to save profile'
        alert('Failed to update profile. Please try again.')
      } finally {
        this.saving = false
      }
    }
  }
}
</script>

<style scoped>
.profile-management {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  position: relative;
  overflow: hidden;
}

/* Background Elements */
.dashboard-bg {
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

/* Dashboard Content */
.dashboard-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

/* Header */
.dashboard-header {
  text-align: center;
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-subtitle {
  color: #94a3b8;
  font-size: 1.1rem;
}

/* Form Sections */
.dashboard-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease;
}

.dashboard-section:hover {
  transform: translateY(-5px);
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: #fff;
  font-size: 1.25rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.section-header h2 svg {
  width: 24px;
  height: 24px;
  color: #6366f1;
}

/* Form Groups */
.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: #94a3b8;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group label::after {
  content: "*";
  color: #f87171;
  margin-left: 4px;
}

.input-wrapper select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpath d='M6 9l6 6 6-6'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.2em;
  padding-right: 3rem;
}

.input-wrapper select option {
  background-color: #1e1b4b;
  color: #fff;
  padding: 0.75rem;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  padding: 1rem 0;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn svg {
  width: 20px;
  height: 20px;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.save-btn {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
}

.save-btn:hover:not(:disabled) {
  background: rgba(34, 197, 94, 0.2);
}

/* Loading & Error States */
.loading,
.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  text-align: center;
}

.loading {
  color: #94a3b8;
}

.error-message {
  color: #f87171;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Completion Warning */
.completion-warning {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: rgba(234, 179, 8, 0.1);
  border-color: rgba(234, 179, 8, 0.2);
  color: #fbbf24;
}

.completion-warning svg {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.completion-warning p {
  margin: 0;
  font-size: 0.95rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-content {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 2rem;
  }

  .dashboard-section {
    padding: 1.25rem;
  }

  .form-actions {
    padding: 1rem 0;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.75rem;
  }

  .header-subtitle {
    font-size: 1rem;
  }

  .section-header h2 {
    font-size: 1.1rem;
  }

  .input-wrapper input,
  .input-wrapper select,
  .input-wrapper textarea {
    font-size: 0.9rem;
    padding: 0.75rem 1rem 0.75rem 2.75rem;
  }

  .input-wrapper svg {
    width: 18px;
    height: 18px;
    left: 0.75rem;
  }
}

/* Focus States */
.input-wrapper input:focus-visible,
.input-wrapper select:focus-visible,
.input-wrapper textarea:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.4);
}

/* Input Number Spinner Removal */
.input-wrapper input[type="number"]::-webkit-inner-spin-button,
.input-wrapper input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.input-wrapper input[type="number"] {
  -moz-appearance: textfield;
}

/* Hover Effects */
.dashboard-section {
  transition: all 0.3s ease;
}

.dashboard-section:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
/* Input Wrapper Fixes */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper svg {
  position: absolute;
  left: 1rem;
  width: 20px;
  height: 20px;
  color: #6366f1;
  top: 50%;
  transform: translateY(-50%);
  pointer-events: none;
}

/* Specific adjustment for textarea icon */
.input-wrapper textarea + svg {
  top: 1.25rem;
  transform: none;
}

/* Input Spacing */
.input-wrapper input,
.input-wrapper select {
  height: 2.75rem;
  padding: 0.5rem 1rem 0.5rem 3rem;
}

.input-wrapper textarea {
  padding: 1rem 1rem 1rem 3rem;
  line-height: 0.13;
}

/* Select specific alignment */
.input-wrapper select {
  padding-right: 3rem;
  background-position: right 1rem center;
}

/* Edge cases for different input types */
.input-wrapper input[type="number"] {
  padding-right: 1rem;
}

/* Focus state maintaining alignment */
.input-wrapper input:focus,
.input-wrapper select:focus,
.input-wrapper textarea:focus {
  border-color: #6366f1;
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* Ensuring consistent height for all input types */
.input-wrapper input,
.input-wrapper select,
.input-wrapper textarea {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #fff;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

</style>