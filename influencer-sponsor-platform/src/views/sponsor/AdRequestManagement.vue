<template>
  <div class="ad-request-management">
    <!-- Background Elements -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="dashboard-content">
      <div class="dashboard-header">
        <h1>Ad Request Management</h1>
        <p class="header-subtitle">Monitor and manage your campaign requests</p>
      </div>

      <!-- Stats Overview -->
      <div class="dashboard-section stats-panel">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-title">Total Requests</div>
              <div class="stat-value">{{ requests.length }}</div>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l4 4L7 17l-4-4L13 3z"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-title">Pending</div>
              <div class="stat-value">
                {{ requests.filter(r => r.status === 'pending').length }}
              </div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-title">Accepted</div>
              <div class="stat-value">
                {{ requests.filter(r => r.status === 'accepted').length }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="dashboard-section filters-section">
        <div class="section-header">
          <h2>Filters</h2>
        </div>
        <div class="filters">
          <div class="filter-group">
            <label>Status</label>
            <select v-model="statusFilter" class="filter-select">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="accepted">Accepted</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Sort By</label>
            <select v-model="sortBy" class="filter-select">
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Campaign</label>
            <select v-model="campaignFilter" class="filter-select">
              <option value="">All Campaigns</option>
              <option v-for="campaign in campaigns" 
                      :key="campaign.id" 
                      :value="campaign.id">
                {{ campaign.title }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading & Error States -->
      <div v-if="loading" class="loading">
        <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
        </svg>
        Loading ad requests...
      </div>
      
      <div v-if="error" class="error-message">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
          <path d="M12 8v5M12 16h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        {{ error }}
      </div>

      <!-- Requests List -->
      <div v-if="!loading && filteredRequests.length" class="requests-list">
        <div v-for="request in filteredRequests" 
             :key="request.id" 
             class="dashboard-section request-card">
          <div class="request-header">
            <div class="campaign-info">
              <h3>{{ getCampaignTitle(request.campaign_id) }}</h3>
              <span :class="['status-badge', request.status]">
                {{ request.status }}
              </span>
            </div>
            <div class="date-info">
              <div class="date-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                {{ formatDate(request.created_at) }}
              </div>
            </div>
          </div>

          <div class="request-body">
            <div class="influencer-details">
              <h4>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                Influencer Details
              </h4>
              <div v-if="getInfluencerDetails(request.influencer_id)" class="details-content">
                <div class="detail-item">
                  <strong>Name:</strong> 
                  {{ getInfluencerDetails(request.influencer_id).name }}
                </div>
                <div class="detail-item">
                  <strong>Category:</strong> 
                  {{ getInfluencerDetails(request.influencer_id).category }}
                </div>
                <div class="detail-item">
                  <strong>Reach:</strong> 
                  {{ formatNumber(getInfluencerDetails(request.influencer_id).reach) }}
                </div>
                <div class="detail-item">
                  <strong>Engagement Rate:</strong> 
                  {{ getInfluencerDetails(request.influencer_id).engagement_rate }}%
                </div>
              </div>
              <div v-else class="fallback-details">
                <div class="detail-item">
                  <strong>ID:</strong> {{ request.influencer_id }}
                </div>
                <div class="detail-item">
                  <em>Additional details unavailable</em>
                </div>
              </div>
            </div>

            <div class="request-details">
              <h4>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
                Request Details
              </h4>
              <div class="details-content">
                <div class="detail-item">
                  <strong>Status:</strong> 
                  <span :class="['status-text', request.status]">
                    {{ request.status }}
                  </span>
                </div>
                <div class="detail-item">
                  <strong>Budget:</strong> 
                  ${{ formatNumber(request.budget || 0) }}
                </div>
                <div class="detail-item">
                  <strong>Platform:</strong> 
                  {{ request.platform || 'Not specified' }}
                </div>
                <div class="detail-item description">
                  <strong>Details:</strong>
                  <p>{{ request.details || 'No additional details provided' }}</p>
                </div>
                <div v-if="request.updated_at !== request.created_at" class="detail-item">
                  <strong>Last Updated:</strong> 
                  {{ formatDate(request.updated_at) }}
                </div>
              </div>
            </div>
          </div>

          <div class="request-actions">
            <button v-if="request.status === 'pending'" 
                    @click="deleteRequest(request.id)" 
                    :disabled="isProcessing === request.id" 
                    class="action-btn delete-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
              {{ isProcessing === request.id ? 'Canceling...' : 'Cancel Request' }}
            </button>

            <button @click="viewDetails(request)" 
                    class="action-btn view-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              View Details
            </button>

            <button v-if="request.status === 'accepted'" 
                    @click="exportDetails(request)"
                    class="action-btn export-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
              </svg>
              Export Details
            </button>
          </div>
        </div>
      </div>

      <!-- No Requests Message -->
      <div v-if="!loading && !filteredRequests.length" class="no-data dashboard-section">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <p>No ad requests found</p>
        <button @click="clearFilters" class="action-btn">Clear Filters</button>
      </div>

      <!-- Details Modal -->
      <Transition name="modal">
        <div v-if="showDetailsModal" class="modal" @click.self="showDetailsModal = false">
          <div class="modal-content">
            <div class="modal-header">
              <h2>Request Details</h2>
              <button class="modal-close" @click="showDetailsModal = false">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <div class="modal-body" v-if="selectedRequest">
              <!-- Campaign Section -->
              <div class="modal-section">
                <h3>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                  Campaign Information
                </h3>
                <div class="detail-grid">
                  <div class="detail-item">
                    <div class="detail-label">Campaign Name</div>
                    <div class="detail-value">{{ getCampaignTitle(selectedRequest.campaign_id) }}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Status</div>
                    <div class="status-indicator" :class="selectedRequest.status">
                      <svg v-if="selectedRequest.status === 'pending'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <svg v-else-if="selectedRequest.status === 'accepted'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      {{ selectedRequest.status }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Influencer Section -->
              <div class="modal-section">
                <h3>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  Influencer Information
                </h3>
                <div class="detail-grid">
                  <div class="detail-item">
                    <div class="detail-label">Name</div>
                    <div class="detail-value">{{ selectedInfluencer.name }}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Category</div>
                    <div class="detail-value">{{ selectedInfluencer.category }}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Reach</div>
                    <div class="detail-value">{{ formatNumber(selectedInfluencer.reach) }}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Engagement Rate</div>
                    <div class="detail-value">{{ selectedInfluencer.engagement_rate }}%</div>
                  </div>
                </div>
              </div>

              <!-- Request Details Section -->
              <div class="modal-section">
                <h3>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  Request Details
                </h3>
                <div class="detail-grid">
                  <div class="detail-item">
                    <div class="detail-label">Submitted Date</div>
                    <div class="detail-value">{{ formatDate(selectedRequest.created_at) }}</div>
                  </div>
                  <div class="detail-item">
                    <div class="detail-label">Last Updated</div>
                    <div class="detail-value">{{ formatDate(selectedRequest.updated_at) }}</div>
                  </div>
                  <div class="detail-item" style="grid-column: 1 / -1">
                    <div class="detail-label">Additional Details</div>
                    <div class="detail-value">{{ selectedRequest.details || 'No additional details provided' }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button @click="showDetailsModal = false" class="action-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 18L18 6M6 6l12 12"/>
                </svg>
                Close
              </button>
              
              <button v-if="selectedRequest?.status === 'accepted'"
                      @click="exportDetails(selectedRequest)"
                      class="action-btn export-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                </svg>
                Export Details
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const FALLBACK_INFLUENCER = {
  name: 'Unknown Influencer',
  category: 'Not Available',
  reach: 0,
  engagement_rate: 0,
  niche: 'Unknown',
  platform: 'Not Specified'
}

export default {
  name: 'AdRequestManagement',
  
  data: () => ({
    requests: [],
    campaigns: [],
    influencerDetails: {},
    loading: true,
    error: null,
    isProcessing: null,
    statusFilter: '',
    campaignFilter: '',
    sortBy: 'newest',
    showDetailsModal: false,
    selectedRequest: null,
    selectedInfluencer: null,
    retryAttempts: 0,
    maxRetries: 3,
    lastFetchTime: null,
    cacheTimeout: 5 * 60 * 1000, // 5 minutes
    exportStatus: {}
  }),

  computed: {
    filteredRequests() {
      let filtered = [...this.requests]
      
      if (this.statusFilter) {
        filtered = filtered.filter((request) => request.status === this.statusFilter)
      }

      if (this.campaignFilter) {
        filtered = filtered.filter((request) => request.campaign_id === this.campaignFilter)
      }

      filtered.sort((a, b) => {
        const dateA = new Date(a.created_at)
        const dateB = new Date(b.created_at)
        return this.sortBy === 'newest' ? dateB - dateA : dateA - dateB
      })

      return filtered
    },

    hasActiveFilters() {
      return this.statusFilter || this.campaignFilter || this.sortBy !== 'newest'
    }
  },

  mounted() {
    this.fetchData()
  },

  methods: {
    formatDate(dateString) {
      if (!dateString) return 'Date not available'
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    formatNumber(num) {
      if (num === null || num === undefined) return 'N/A'
      return new Intl.NumberFormat().format(num)
    },

    getCampaignTitle(campaignId) {
      const campaign = this.campaigns.find((c) => c.id === campaignId)
      return campaign ? campaign.title : 'Unknown Campaign'
    },

    getInfluencerDetails(influencerId) {
      return this.influencerDetails[influencerId] || FALLBACK_INFLUENCER
    },

    async fetchData(retrying = false) {
      if (!retrying) {
        this.loading = true
        this.error = null
      }

      try {
        const now = Date.now()
        if (this.lastFetchTime && (now - this.lastFetchTime < this.cacheTimeout)) {
          this.loading = false
          return
        }

        await Promise.all([
          this.fetchRequests(),
          this.fetchCampaigns()
        ])

        this.lastFetchTime = now
        this.retryAttempts = 0
        this.error = null
      } catch (error) {
        console.error('Error fetching data:', error)
        
        if (this.retryAttempts < this.maxRetries) {
          this.retryAttempts += 1
          setTimeout(() => this.fetchData(true), 1000 * this.retryAttempts)
        } else {
          this.error = 'Unable to load data. Please try again later.'
        }
      } finally {
        this.loading = false
      }
    },

    async fetchRequests() {
      const { data } = await axios.get('/ad_requests')
      this.requests = data
      await this.fetchInfluencerDetails()
    },

    async fetchCampaigns() {
      const { data } = await axios.get('/campaigns')
      this.campaigns = data
    },

    async fetchInfluencerDetails() {
      const uniqueInfluencerIds = [...new Set(this.requests.map((r) => r.influencer_id))]
      
      const promises = uniqueInfluencerIds.map(async (id) => {
        try {
          const { data } = await axios.get(`/influencer/${id}`)
          this.$set(this.influencerDetails, id, {
            ...FALLBACK_INFLUENCER,
            ...data
          })
        } catch (error) {
          console.error(`Error fetching influencer ${id}:`, error)
          this.$set(this.influencerDetails, id, FALLBACK_INFLUENCER)
        }
      })

      await Promise.allSettled(promises)
    },

    async deleteRequest(requestId) {
      if (!window.confirm('Are you sure you want to cancel this request? This action cannot be undone.')) {
        return
      }

      try {
        this.isProcessing = requestId
        await axios.delete(`/sponsor_ad_request/${requestId}`)
        this.requests = this.requests.filter((r) => r.id !== requestId)
        this.$emit('request-deleted', requestId)
        this.showSuccessMessage('Request canceled successfully')
      } catch (error) {
        console.error('Error canceling request:', error)
        this.showErrorMessage('Failed to cancel request. Please try again.')
      } finally {
        this.isProcessing = null
      }
    },

    viewDetails(request) {
      this.selectedRequest = request
      this.selectedInfluencer = this.getInfluencerDetails(request.influencer_id)
      this.showDetailsModal = true
    },

    async exportDetails(request) {
      if (this.exportStatus[request.id] === 'processing') return

      try {
        this.$set(this.exportStatus, request.id, 'processing')
        
        const campaign = this.campaigns.find((c) => c.id === request.campaign_id)
        const influencer = this.getInfluencerDetails(request.influencer_id)
        
        const exportData = {
          campaign_details: campaign,
          influencer_details: influencer,
          request_details: request,
          export_date: new Date().toISOString()
        }

        const { data } = await axios.post('/export_request_details', exportData)
        const blob = new Blob([JSON.stringify(data, null, 2)], { 
          type: 'application/json' 
        })
        const url = window.URL.createObjectURL(blob)
        
        const link = document.createElement('a')
        link.href = url
        link.download = `request-${request.id}-details.json`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)

        this.showSuccessMessage('Export completed successfully')
      } catch (error) {
        console.error('Export error:', error)
        this.showErrorMessage('Failed to export details. Please try again.')
      } finally {
        this.$set(this.exportStatus, request.id, 'completed')
        setTimeout(() => {
          this.$delete(this.exportStatus, request.id)
        }, 3000)
      }
    },

    clearFilters() {
      this.statusFilter = ''
      this.campaignFilter = ''
      this.sortBy = 'newest'
    },

    showSuccessMessage(message) {
      // Implement your success notification method here
      console.log('Success:', message)
    },

    showErrorMessage(message) {
      // Implement your error notification method here
      console.error('Error:', message)
    }
  },

  beforeUnmount() {
    // Clean up any pending operations
    Object.keys(this.exportStatus).forEach((id) => {
      this.$delete(this.exportStatus, id)
    })
  }
}
</script>

<style scoped>

<style scoped>
.filter-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 0.75rem;
  border-radius: 12px;
  outline: none;
  width: 100%;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  -webkit-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1em;
  padding-right: 2.5rem;
}

.filter-select:hover {
  background-color: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.filter-select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* Style for the options within select */
.filter-select option {
  background-color: #1e1b4b;
  color: #fff;
  padding: 0.75rem;
}

.filter-select option:hover {
  background-color: #2d2a5d;
}

/* For Firefox - darker dropdown background */
.filter-select:-moz-focusring {
  color: transparent;
  text-shadow: 0 0 0 #fff;
}

@-moz-document url-prefix() {
  .filter-select {
    color: #fff;
    background-color: #1e1b4b;
  }
}

/* For IE/Edge - darker dropdown background */
.filter-select::-ms-expand {
  display: none;
}

.filter-select::-ms-value {
  background-color: #1e1b4b;
  color: #fff;
}

.ad-request-management {
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
}

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

/* Stats Panel */
.stats-panel {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.stat-icon {
  width: 40px;
  height: 40px;
  color: #6366f1;
}

.stat-content {
  flex: 1;
}

.stat-title {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.stat-value {
  color: #fff;
  font-size: 1.5rem;
  font-weight: 600;
}

/* Dashboard Section Styling */
.dashboard-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease;
  margin-bottom: 1.5rem;
}

.dashboard-section:hover {
  transform: translateY(-5px);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: #fff;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

/* Filters Section */
.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  color: #94a3b8;
  font-weight: 500;
}

.filter-select {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 0.75rem;
  border-radius: 12px;
  outline: none;
  transition: all 0.3s ease;
}

.filter-select:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
}

.filter-select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
}

/* Request Cards */
.request-card {
  margin-bottom: 1.5rem;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.campaign-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.campaign-info h3 {
  color: #fff;
  margin: 0;
  font-size: 1.25rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-badge.pending {
  background: rgba(234, 179, 8, 0.2);
  color: #fbbf24;
}

.status-badge.accepted {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.status-badge.rejected {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.date-info {
  color: #94a3b8;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date-item svg {
  width: 16px;
  height: 16px;
  color: #6366f1;
}

/* Request Body */
.request-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.influencer-details,
.request-details {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.influencer-details h4,
.request-details h4 {
  color: #fff;
  margin: 0 0 1rem 0;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.influencer-details h4 svg,
.request-details h4 svg {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

.details-content {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.detail-item {
  color: #94a3b8;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.detail-item strong {
  color: #fff;
  min-width: 120px;
}

.detail-item.description {
  flex-direction: column;
}

.detail-item.description p {
  margin: 0.5rem 0 0 0;
  line-height: 1.5;
}

.fallback-details {
  padding: 1rem;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.fallback-details em {
  color: #f87171;
}

/* Request Actions */
.request-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  font-size: 0.875rem;
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

.action-btn.delete-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

.action-btn.delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.action-btn.view-btn {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
}

.action-btn.view-btn:hover {
  background: rgba(59, 130, 246, 0.2);
}

.action-btn.export-btn {
  background: rgba(139, 92, 246, 0.1);
  color: #a78bfa;
}

.action-btn.export-btn:hover {
  background: rgba(139, 92, 246, 0.2);
}

/* Loading and Error States */
.loading,
.error-message,
.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  text-align: center;
  flex-direction: column;
}

.loading {
  color: #94a3b8;
}

.loading .spinner {
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

.error-message {
  color: #f87171;
}

.error-icon {
  width: 40px;
  height: 40px;
}

.no-data {
  color: #94a3b8;
}

.no-data svg {
  width: 48px;
  height: 48px;
  color: #6366f1;
  opacity: 0.5;
}

.no-data p {
  font-size: 1.1rem;
  margin: 0.5rem 0 1rem;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-content {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 2rem;
  }

  .request-body {
    grid-template-columns: 1fr;
  }

  .filters {
    grid-template-columns: 1fr;
  }

  .request-actions {
    flex-wrap: wrap;
  }

  .action-btn {
    flex: 1;
    min-width: 140px;
  }

  .modal {
    padding: 0.5rem;
  }
}

@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.75rem;
  }

  .request-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-icon {
    width: 32px;
    height: 32px;
  }

  .stat-value {
    font-size: 1.25rem;
  }
}

/* Modal Styles */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  color: #fff;
  font-size: 1.5rem;
  margin: 0;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.modal-close {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  color: #fff;
  transform: rotate(90deg);
}

.modal-close svg {
  width: 24px;
  height: 24px;
}

.modal-body {
  margin-bottom: 2rem;
}

.modal-section {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-section h3 {
  color: #fff;
  font-size: 1.25rem;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-section h3 svg {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.detail-item {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-label {
  color: #94a3b8;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.detail-value {
  color: #fff;
  font-size: 1rem;
  font-weight: 500;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Modal Transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}

/* Status Indicators */
.status-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  padding: 0.375rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  width: fit-content;
}

.status-indicator.pending {
  background: rgba(234, 179, 8, 0.2);
  color: #fbbf24;
}

.status-indicator.accepted {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.status-indicator.rejected {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.status-indicator svg {
  width: 16px;
  height: 16px;
}
</style>