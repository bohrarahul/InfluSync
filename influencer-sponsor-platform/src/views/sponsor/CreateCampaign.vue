<template>
  <div class="create-campaign">
    <!-- Background circles -->
    <div class="campaign-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="campaign-content">
      <div class="page-header">
        <h1>Create New Campaign</h1>
        <p class="header-subtitle">Launch your marketing initiative</p>
      </div>

      <form @submit.prevent="createCampaign" class="campaign-form">
        <div class="form-group">
          <label for="title">Campaign Title</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            <input
              id="title"
              v-model="form.title"
              type="text"
              required
              placeholder="Enter campaign title"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon textarea-icon">
              <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
            <textarea
              id="description"
              v-model="form.description"
              rows="4"
              required
              placeholder="Describe your campaign"
            ></textarea>
          </div>
        </div>

        <div class="form-group">
          <label for="budget">Budget</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M12 1v22M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/>
            </svg>
            <input
              id="budget"
              v-model.number="form.budget"
              type="number"
              step="0.01"
              required
              placeholder="Enter campaign budget"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="category">Category</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M20 7h-7L10 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2V9a2 2 0 00-2-2z"/>
            </svg>
            <input
              id="category"
              v-model="form.category"
              type="text"
              required
              placeholder="Enter campaign category"
            >
          </div>
        </div>

        <div class="date-group">
          <div class="form-group">
            <label for="start_date">Start Date</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              <input
                id="start_date"
                v-model="form.start_date"
                type="date"
                required
              >
            </div>
          </div>

          <div class="form-group">
            <label for="end_date">End Date</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
              </svg>
              <input
                id="end_date"
                v-model="form.end_date"
                type="date"
                required
              >
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-create" :disabled="creating">
            <span v-if="creating">
              <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              Creating...
            </span>
            <span v-else>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="btn-icon">
                <path d="M12 5v14M5 12h14"/>
              </svg>
              Create Campaign
            </span>
          </button>
          <button
            type="button"
            class="btn-cancel"
            @click="$router.push('/sponsor/campaigns')"
            :disabled="creating"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CreateCampaign',
  data() {
    return {
      form: {
        title: '',
        description: '',
        budget: null,
        category: '',
        start_date: '',
        end_date: '',
        status: 'active'
      },
      creating: false
    }
  },
  methods: {
    async createCampaign() {
      try {
        this.creating = true
        await axios.post('/campaigns', this.form)
        this.$router.push('/sponsor/campaigns')
      } catch (err) {
        console.error('Error creating campaign:', err)
        alert('Failed to create campaign')
      } finally {
        this.creating = false
      }
    }
  }
}
</script>

<style scoped>
.create-campaign {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  position: relative;
  overflow: hidden;
  padding: 2rem;
}

/* Background Elements */
.campaign-bg {
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

/* Content Container */
.campaign-content {
  position: relative;
  z-index: 2;
  max-width: 800px;
  margin: 0 auto;
}

/* Header Styles */
.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
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

/* Form Styles */
.campaign-form {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.form-group {
  margin-bottom: 1.5rem;
}

.date-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #94a3b8;
  font-size: 0.875rem;
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

.textarea-icon {
  top: 1.25rem;
}

input, textarea {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

textarea {
  min-height: 120px;
  resize: vertical;
  padding-top: 1.25rem;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.08);
}

input::placeholder, textarea::placeholder {
  color: #64748b;
}

/* Calendar Input Styling */
input[type="date"] {
  appearance: none;
  -webkit-appearance: none;
  padding-right: 1rem;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  background: none;
  cursor: pointer;
  position: absolute;
  right: 1rem;
  filter: invert(1) opacity(0.5);
}

/* Form Actions */
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-create, .btn-cancel {
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-create {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white;
  flex: 1;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  padding: 0.875rem 2rem;
}

.btn-create:hover, .btn-cancel:hover {
  transform: translateY(-2px);
}

.btn-icon, .spinner {
  width: 20px;
  height: 20px;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

button:disabled {
  background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
  cursor: not-allowed;
  transform: none;
}

/* Responsive Design */
@media (max-width: 768px) {
  .create-campaign {
    padding: 1rem;
  }

  .campaign-form {
    padding: 1.5rem;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .date-group {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-create, .btn-cancel {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .page-header h1 {
    font-size: 1.75rem;
  }

  .form-group {
    margin-bottom: 1.25rem;
  }
}
</style>