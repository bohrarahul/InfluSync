<template>
  <div class="sponsor-profile">
    <!-- View Mode -->
    <div v-if="!isEditing" class="profile-view">
      <div class="profile-header">
        <div class="profile-pic-container">
          <img 
            :src="profile.profile_pic || '/default-profile.jpg'" 
            alt="Profile"
            class="profile-pic"
          >
          <div class="profile-pic-overlay">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="camera-icon">
              <path d="M23 19a2 2 0 01-2 2H3a2 2 0 01-2-2V8a2 2 0 012-2h4l2-3h6l2 3h4a2 2 0 012 2z"/>
              <circle cx="12" cy="13" r="4"/>
            </svg>
          </div>
        </div>
        <button @click="isEditing = true" class="btn-edit">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="edit-icon">
            <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
          Edit Profile
        </button>
      </div>
      
      <div class="profile-info">
        <div class="info-group">
          <div class="info-label">Company</div>
          <div class="info-value">{{ profile.company_name || 'Not set' }}</div>
        </div>
        <div class="info-group">
          <div class="info-label">Industry</div>
          <div class="info-value">{{ profile.industry || 'Not set' }}</div>
        </div>
        <div class="info-group">
          <div class="info-label">Budget</div>
          <div class="info-value">${{ profile.budget || '0' }}</div>
        </div>
        <div class="info-group">
          <div class="info-label">Description</div>
          <div class="info-value description">{{ profile.description || 'Not set' }}</div>
        </div>
      </div>
    </div>

    <!-- Edit Mode -->
    <div v-else class="profile-edit">
      <form @submit.prevent="updateProfile" class="edit-form">
        <div class="form-group">
          <label for="company">Company Name</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16"/>
              <path d="M3 21h18"/>
              <path d="M9 7h1M9 11h1M9 15h1M14 7h1M14 11h1M14 15h1"/>
            </svg>
            <input 
              id="company"
              v-model="editedProfile.company_name"
              type="text"
              required
              placeholder="Enter company name"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="industry">Industry</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="input-icon">
              <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/>
              <path d="M3.27 6.96L12 12.01l8.73-5.05"/>
              <path d="M12 22.08V12"/>
            </svg>
            <input 
              id="industry"
              v-model="editedProfile.industry"
              type="text"
              required
              placeholder="Enter industry"
            >
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
              v-model.number="editedProfile.budget"
              type="number"
              step="0.01"
              required
              placeholder="Enter budget"
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
              v-model="editedProfile.description"
              rows="4"
              required
              placeholder="Enter company description"
            ></textarea>
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="btn-save" :disabled="updating">
            <span v-if="updating">
              <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
              </svg>
              Saving...
            </span>
            <span v-else>Save Changes</span>
          </button>
          <button 
            type="button" 
            class="btn-cancel"
            @click="cancelEdit"
            :disabled="updating"
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
  name: 'SponsorProfile',
  props: {
    profile: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isEditing: false,
      updating: false,
      editedProfile: {
        company_name: '',
        industry: '',
        budget: 0,
        description: ''
      }
    }
  },
  watch: {
    profile: {
      handler(newProfile) {
        this.editedProfile = { ...newProfile }
      },
      immediate: true
    }
  },
  methods: {
    async updateProfile() {
      try {
        this.updating = true
        
        // Send as JSON instead of FormData
        await axios.put('/profile', {
          company_name: this.editedProfile.company_name,
          industry: this.editedProfile.industry,
          budget: Number(this.editedProfile.budget),
          description: this.editedProfile.description
        })

        this.isEditing = false
        this.$emit('profile-updated')
      } catch (err) {
        console.error('Error updating profile:', err)
        alert('Failed to update profile: ' + (err.response?.data?.message || err.message))
      } finally {
        this.updating = false
      }
    },
    cancelEdit() {
      this.editedProfile = { ...this.profile }
      this.isEditing = false
    }
  }
}
</script>

<style scoped>
.sponsor-profile {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  padding: 1.5rem;
  color: #fff;
}

/* Profile Header */
.profile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.profile-pic-container {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
}

.profile-pic {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.profile-pic-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.profile-pic-container:hover .profile-pic {
  transform: scale(1.1);
}

.profile-pic-container:hover .profile-pic-overlay {
  opacity: 1;
}

.camera-icon {
  width: 24px;
  height: 24px;
  color: white;
}

/* Button Styles */
.btn-edit, .btn-save, .btn-cancel {
  padding: 0.75rem 1.5rem;
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

.btn-edit {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white;
}

.btn-edit:hover {
  transform: translateY(-2px);
}

.btn-save {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}

.btn-save:hover, .btn-cancel:hover {
  transform: translateY(-2px);
}

button:disabled {
  background: linear-gradient(135deg, #4b5563 0%, #374151 100%);
  cursor: not-allowed;
  transform: none;
}

/* Profile Info */
.profile-info {
  display: grid;
  gap: 1.5rem;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-label {
  color: #94a3b8;
  font-size: 0.875rem;
  font-weight: 500;
}

.info-value {
  color: #fff;
  font-size: 1rem;
}

.info-value.description {
  line-height: 1.5;
}

/* Form Styles */
.edit-form {
  display: grid;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
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
  min-height: 100px;
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

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

/* Loading Spinner */
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

/* Responsive Design */
@media (max-width: 640px) {
  .sponsor-profile {
    padding: 1rem;
  }

  .profile-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .profile-pic-container {
    width: 100px;
    height: 100px;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn-edit, .btn-save, .btn-cancel {
    width: 100%;
    justify-content: center;
  }
}
</style>