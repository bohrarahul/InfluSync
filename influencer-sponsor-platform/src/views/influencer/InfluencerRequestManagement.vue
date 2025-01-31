<template>
  <div class="request-management">
    <!-- Background Elements -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="content-wrapper">
      <h1>Ad Requests Management</h1>

      <!-- Filters -->
      <div class="filters-section">
        <div class="filters">
          <div class="filter-group">
            <label>Status:</label>
            <select v-model="statusFilter">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="accepted">Accepted</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>

          <div class="filter-group">
            <label>Sort By:</label>
            <select v-model="sortBy">
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Loading & Error States -->
      <div v-if="loading" class="loading">Loading requests...</div>
      <div v-if="error" class="error-message">{{ error }}</div>

      <!-- Requests List -->
      <div v-if="!loading && filteredRequests.length" class="requests-list">
        <div v-for="request in filteredRequests" 
             :key="request.id" 
             class="request-card">
          <div class="request-header">
            <div class="campaign-info">
              <h3>{{ getCampaignTitle(request.campaign_id) }}</h3>
              <span :class="['status-badge', request.status]">
                {{ request.status }}
              </span>
            </div>
            <div class="date-info">
              Received: {{ formatDate(request.created_at) }}
            </div>
          </div>

          <div class="request-body">
            <div class="campaign-details" v-if="campaignDetails[request.campaign_id]">
              <div class="detail-row">
                <strong>Budget:</strong> 
                <span>${{ campaignDetails[request.campaign_id].budget }}</span>
              </div>
              <div class="detail-row">
                <strong>Category:</strong> 
                <span>{{ campaignDetails[request.campaign_id].category }}</span>
              </div>
              <div class="detail-row">
                <strong>Duration:</strong> 
                <span>
                  {{ formatDate(campaignDetails[request.campaign_id].start_date) }} - 
                  {{ formatDate(campaignDetails[request.campaign_id].end_date) }}
                </span>
              </div>
            </div>

            <div class="request-details">
              <p><strong>Message from Sponsor:</strong></p>
              <p class="request-message">{{ request.details || 'No additional details provided' }}</p>
            </div>
          </div>

          <div class="request-actions">
            <!-- Actions for Pending Requests -->
            <template v-if="request.status === 'pending'">
              <button 
                @click="handleRequest(request.id, 'accept')"
                :disabled="processingId === request.id"
                class="accept-btn"
              >
                {{ processingId === request.id ? 'Accepting...' : 'Accept Request' }}
              </button>
              <button 
                @click="handleRequest(request.id, 'reject')"
                :disabled="processingId === request.id"
                class="reject-btn"
              >
                {{ processingId === request.id ? 'Rejecting...' : 'Reject Request' }}
              </button>
            </template>

            <!-- Contact for Negotiation -->
            <button 
              v-if="!showNegotiationEmail[request.id]"
              @click="toggleNegotiationEmail(request.id)"
              class="negotiate-btn"
            >
              Contact for Negotiation
            </button>

            <!-- Negotiation Email Section -->
            <div v-if="showNegotiationEmail[request.id]" class="negotiation-details">
              <p>Sponsor Email: 
                <a :href="'mailto:' + getSponsorEmail(request.campaign_id)">
                  {{ getSponsorEmail(request.campaign_id) }}
                </a>
              </p>
              <div class="email-note">
                <i>Note: Please reference Request ID #{{ request.id }} in your communication</i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- No Requests Message -->
      <div v-if="!loading && !filteredRequests.length" class="no-data">
        <p>No ad requests found</p>
        <p class="suggestion">Try adjusting your filters or check back later for new requests.</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'InfluencerRequestManagement',
  data() {
    return {
      requests: [],
      campaignDetails: {},
      sponsorEmails: {},
      loading: true,
      error: null,
      processingId: null,
      statusFilter: '',
      sortBy: 'newest',
      showNegotiationEmail: {}
    }
  },
  computed: {
    filteredRequests() {
      let filtered = [...this.requests]
      
      if (this.statusFilter) {
        filtered = filtered.filter(request => request.status === this.statusFilter)
      }

      filtered.sort((a, b) => {
        const dateA = new Date(a.created_at)
        const dateB = new Date(b.created_at)
        return this.sortBy === 'newest' ? dateB - dateA : dateA - dateB
      })

      return filtered
    }
  },
  created() {
    this.fetchRequests()
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    async fetchRequests() {
      try {
        this.loading = true
        const response = await axios.get('/influencer_ad_requests')
        this.requests = response.data

        // Fetch campaign details for each request
        const campaignIds = [...new Set(this.requests.map(r => r.campaign_id))]
        await Promise.all(campaignIds.map(this.fetchCampaignDetails))
      } catch (err) {
        console.error('Error fetching requests:', err)
        this.error = 'Failed to load requests'
      } finally {
        this.loading = false
      }
    },
    async fetchCampaignDetails(campaignId) {
      try {
        const response = await axios.get(`/campaigns/${campaignId}`)
        this.$set(this.campaignDetails, campaignId, response.data)
        if (response.data.sponsor) {
          this.$set(this.sponsorEmails, campaignId, response.data.sponsor.email)
        }
      } catch (err) {
        console.error(`Error fetching campaign ${campaignId}:`, err)
      }
    },
    getCampaignTitle(campaignId) {
      return this.campaignDetails[campaignId]?.title || 'Loading...'
    },
    getSponsorEmail(campaignId) {
      return this.sponsorEmails[campaignId] || 'Loading...'
    },
    async handleRequest(requestId, action) {
      if (!confirm(`Are you sure you want to ${action} this request?`)) return

      try {
        this.processingId = requestId
        await axios.put('/influencer_ad_requests', {
          ad_request_id: requestId,
          action
        })
        
        // Update request status locally
        const request = this.requests.find(r => r.id === requestId)
        if (request) {
          request.status = action === 'accept' ? 'accepted' : 'rejected'
        }

        alert(`Request ${action}ed successfully`)
      } catch (err) {
        console.error('Error handling request:', err)
        alert(`Failed to ${action} request`)
      } finally {
        this.processingId = null
      }
    },
    toggleNegotiationEmail(requestId) {
      this.$set(this.showNegotiationEmail, requestId, !this.showNegotiationEmail[requestId])
    }
  }
}
</script>

<style scoped>
.request-management {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  padding: 2rem;
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
  right: -100px;
  animation: float 20s infinite;
}

.circle-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%);
  bottom: 40%;
  left: -200px;
  animation: float 25s infinite reverse;
}

.circle-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%);
  bottom: -50px;
  right: 10%;
  animation: float 15s infinite;
}

@keyframes float {
  0% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(30px, -30px) rotate(120deg); }
  66% { transform: translate(-20px, 20px) rotate(240deg); }
  100% { transform: translate(0, 0) rotate(360deg); }
}

.content-wrapper {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  color: white;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
}

.filters-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

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
  font-size: 0.9rem;
}

.filter-group select {
  width: 100%;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  cursor: pointer;
}

.filter-group select:hover {
  background: rgba(255, 255, 255, 0.08);
}

.filter-group select:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.5);
}

.filter-group select option {
  background: #1e1b4b;
  color: #e2e8f0;
  padding: 0.5rem;
}

.request-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.request-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.campaign-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.campaign-info h3 {
  color: white;
  margin: 0;
  font-size: 1.25rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.pending {
  background: rgba(234, 179, 8, 0.1);
  color: #eab308;
  border: 1px solid rgba(234, 179, 8, 0.2);
}

.status-badge.accepted {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.status-badge.rejected {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.date-info {
  color: #94a3b8;
  font-size: 0.9rem;
}

.request-body {
  margin-bottom: 1.5rem;
}

.campaign-details, .request-details {
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  margin-bottom: 1.25rem;
}

.detail-row {
  margin-bottom: 0.75rem;
  color: #94a3b8;
}

.detail-row strong {
  color: white;
  margin-right: 0.5rem;
}

.request-details {
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  margin-top: 1.25rem;
}

.request-details p {
  margin: 0;
}

.request-details p strong {
  color: #e2e8f0;
  font-size: 0.95rem;
  font-weight: 500;
  display: block;
  margin-bottom: 0.75rem;
}

.request-message {
  color: #94a3b8;
  line-height: 1.6;
  font-size: 0.95rem;
  white-space: pre-wrap;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

/* Empty state styling */
.request-message:empty::before,
.request-message:blank::before {
  content: 'No additional details provided';
  color: #64748b;
  font-style: italic;
}

.request-message {
  color: #94a3b8;
  white-space: pre-wrap;
  line-height: 1.6;
}

.request-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.request-actions button {
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: 1px solid transparent;
}

.accept-btn {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border-color: rgba(16, 185, 129, 0.2);
}

.reject-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.2);
}

.negotiate-btn {
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
  border-color: rgba(99, 102, 241, 0.2);
}

.request-actions button:hover {
  transform: translateY(-2px);
}

.accept-btn:hover {
  background: rgba(16, 185, 129, 0.2);
}

.reject-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

.negotiate-btn:hover {
  background: rgba(99, 102, 241, 0.2);
}

.request-actions button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.negotiation-details {
  width: 100%;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  margin-top: 1rem;
  color: #94a3b8;
}

.negotiation-details a {
  color: #818cf8;
  text-decoration: none;
  transition: color 0.3s ease;
}

.negotiation-details a:hover {
  color: #6366f1;
}

.email-note {
  margin-top: 1rem;
  color: #64748b;
  font-size: 0.9rem;
}

.loading, .error-message, .no-data {
  text-align: center;
  padding: 3rem;
  color: #94a3b8;
}

.error-message {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 16px;
}

@media (max-width: 768px) {
  .request-management {
    padding: 1rem;
  }

  .request-header {
    flex-direction: column;
    gap: 1rem;
  }

  .campaign-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .request-actions {
    flex-direction: column;
  }

  .request-actions button {
    width: 100%;
  }
}
</style>