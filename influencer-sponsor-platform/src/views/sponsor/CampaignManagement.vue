<template>
  <div class="campaign-management">
    <!-- Background Elements -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="page-content">
      <div class="page-header">
        <h1>My Campaigns</h1>
        <button @click="$router.push('/sponsor/campaigns/new')" class="create-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          Create New Campaign
        </button>
      </div>

      <!-- Loading & Error States -->
      <div v-if="loading" class="loading">
        <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
        </svg>
        Loading campaigns...
      </div>
      <div v-if="error" class="error-message">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
          <path d="M12 8v5M12 16h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        {{ error }}
      </div>

      <!-- Filters -->
      <div class="filters">
        <div class="search-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="Search campaigns..."
          >
        </div>
        <select v-model="statusFilter">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      <!-- Campaigns List -->
      <div class="campaigns-list" v-if="!loading && filteredCampaigns.length">
        <div 
          v-for="campaign in filteredCampaigns" 
          :key="campaign.id" 
          class="campaign-card"
        >
          <div class="campaign-header">
            <h3>{{ campaign.title }}</h3>
            <span :class="['status-badge', campaign.status]">
              {{ campaign.status }}
            </span>
          </div>

          <div class="campaign-details">
            <p>{{ campaign.description }}</p>
            <div class="campaign-meta">
              <span class="meta-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <strong>Budget:</strong> ${{ campaign.budget }}
              </span>
              <span class="meta-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
                <strong>Category:</strong> {{ campaign.category }}
              </span>
            </div>
            <div class="campaign-dates">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              <span>{{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}</span>
            </div>
          </div>

          <div class="campaign-actions">
            <button 
              @click="editCampaign(campaign)"
              class="edit-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
              </svg>
              Edit
            </button>
            <button 
              @click="deleteCampaign(campaign.id)"
              :disabled="isDeleting === campaign.id"
              class="delete-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              {{ isDeleting === campaign.id ? 'Deleting...' : 'Delete' }}
            </button>
          </div>
        </div>
      </div>

      <!-- No Campaigns Message -->
      <div v-else-if="!loading" class="no-data">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
        <p>No campaigns found. Click "Create New Campaign" to get started.</p>
      </div>

      <!-- Edit Campaign Modal -->
      <div v-if="showEditModal" class="modal">
        <div class="modal-content">
          <h2>Edit Campaign</h2>
          <form @submit.prevent="updateCampaign">
            <!-- Form groups remain the same, styling updated in CSS -->
            <div class="form-group">
              <label>Title</label>
              <input 
                v-model="editingCampaign.title"
                type="text"
                required
              >
            </div>

            <div class="form-group">
              <label>Description</label>
              <textarea 
                v-model="editingCampaign.description"
                rows="4"
                required
              ></textarea>
            </div>

            <div class="form-group">
              <label>Budget</label>
              <input 
                v-model.number="editingCampaign.budget"
                type="number"
                step="0.01"
                required
              >
            </div>

            <div class="form-group">
              <label>Category</label>
              <input 
                v-model="editingCampaign.category"
                type="text"
                required
              >
            </div>

            <div class="form-group">
              <label>Status</label>
              <select v-model="editingCampaign.status">
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
                <option value="completed">Completed</option>
              </select>
            </div>

            <div class="form-group">
              <label>Start Date</label>
              <input 
                v-model="editingCampaign.start_date"
                type="date"
                required
              >
            </div>

            <div class="form-group">
              <label>End Date</label>
              <input 
                v-model="editingCampaign.end_date"
                type="date"
                required
              >
            </div>

            <div class="modal-actions">
              <button type="submit" :disabled="isUpdating" class="save-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 13l4 4L19 7"/>
                </svg>
                {{ isUpdating ? 'Saving...' : 'Save Changes' }}
              </button>
              <button 
                type="button" 
                @click="showEditModal = false"
                :disabled="isUpdating"
                class="cancel-btn"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 18L18 6M6 6l12 12"/>
                </svg>
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CampaignManagement',
  data() {
    return {
      campaigns: [],
      loading: true,
      error: null,
      searchQuery: '',
      statusFilter: '',
      isDeleting: null,
      showEditModal: false,
      isUpdating: false,
      editingCampaign: null
    }
  },
  computed: {
    filteredCampaigns() {
      return this.campaigns.filter(campaign => {
        const matchesSearch = campaign.title.toLowerCase()
          .includes(this.searchQuery.toLowerCase()) ||
          campaign.description.toLowerCase()
          .includes(this.searchQuery.toLowerCase())
        
        const matchesStatus = !this.statusFilter || 
          campaign.status === this.statusFilter

        return matchesSearch && matchesStatus
      })
    }
  },
  created() {
    this.fetchCampaigns()
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    async fetchCampaigns() {
      try {
        this.loading = true
        const response = await axios.get('/campaigns')
        this.campaigns = response.data
        this.error = null
      } catch (err) {
        console.error('Error fetching campaigns:', err)
        this.error = 'Failed to load campaigns'
      } finally {
        this.loading = false
      }
    },
    editCampaign(campaign) {
      this.editingCampaign = { ...campaign }
      this.showEditModal = true
    },
    async updateCampaign() {
      try {
        this.isUpdating = true
        await axios.put(`/campaigns/${this.editingCampaign.id}`, this.editingCampaign)
        
        const index = this.campaigns.findIndex(c => c.id === this.editingCampaign.id)
        if (index !== -1) {
          this.campaigns[index] = { ...this.editingCampaign }
        }
        
        this.showEditModal = false
        this.editingCampaign = null
      } catch (err) {
        console.error('Error updating campaign:', err)
        alert('Failed to update campaign')
      } finally {
        this.isUpdating = false
      }
    },
    async deleteCampaign(campaignId) {
      if (!confirm('Are you sure you want to delete this campaign?')) return

      try {
        this.isDeleting = campaignId
        await axios.delete(`/campaigns/${campaignId}`)
        this.campaigns = this.campaigns.filter(c => c.id !== campaignId)
      } catch (err) {
        console.error('Error deleting campaign:', err)
        alert('Failed to delete campaign')
      } finally {
        this.isDeleting = null
      }
    }
  }
}
</script>

<style scoped>
.campaign-management {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  position: relative;
  overflow: hidden;
}

/* Background Elements - Matching Dashboard */
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

/* Page Content */
.page-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Filters */
.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  flex: 1;
}

.search-box svg {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #94a3b8;
}

.search-box input,
.filters select {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
}

.filters select {
  padding-left: 1rem;
  min-width: 200px;
  cursor: pointer;
}

.filters select option {
  background: #1e1b4b;
  color: white;
}

/* Campaign Cards */
.campaigns-list {
  display: grid;
  gap: 1.5rem;
}

.campaign-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease;
}

.campaign-card:hover {
  transform: translateY(-5px);
}

.campaign-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.campaign-header h3 {
  color: #fff;
  font-size: 1.25rem;
  font-weight: 600;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-badge.inactive {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.status-badge.completed {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.campaign-details {
  color: #94a3b8;
}

.campaign-details p {
  margin-bottom: 1rem;
  line-height: 1.6;
}

.campaign-meta {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-item svg {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

.campaign-dates {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
  font-size: 0.875rem;
}

.campaign-dates svg {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

/* Action Buttons */
.campaign-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.create-btn,
.edit-btn,
.delete-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.edit-btn {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.delete-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.create-btn:hover,
.edit-btn:hover,
.delete-btn:hover {
  transform: translateY(-2px);
}

.create-btn svg,
.edit-btn svg,
.delete-btn svg {
  width: 20px;
  height: 20px;
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #1e1b4b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  color: #94a3b8;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: white;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.save-btn,
.cancel-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-btn {
  background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
  color: white;
  border: none;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.05);
  color: #94a3b8;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Loading and Error States */
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: #94a3b8;
  padding: 2rem;
}

.spinner {
  animation: spin 1s linear infinite;
  width: 24px;
  height: 24px;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.error-icon {
  width: 20px;
  height: 20px;
}

.no-data {
  text-align: center;
  color: #94a3b8;
  padding: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.no-data svg {
  width: 48px;
  height: 48px;
  color: #6366f1;
  opacity: 0.5;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-content {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .page-header h1 {
    font-size: 2rem;
  }

  .filters {
    flex-direction: column;
  }

  .campaign-meta {
    flex-direction: column;
    gap: 1rem;
  }

  .campaign-actions {
    flex-direction: column;
  }

  .modal-content {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .page-header h1 {
    font-size: 1.75rem;
  }

  .campaign-card {
    padding: 1rem;
  }

  .campaign-header {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
}
</style>