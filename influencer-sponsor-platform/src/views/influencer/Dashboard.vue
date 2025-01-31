<template>
  <div class="influencer-dashboard">
    <!-- Background Elements -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="dashboard-content">
      <!-- Dashboard Header -->
      <div class="dashboard-header">
        <div class="header-content">
          <h1>Influencer Dashboard</h1>
          <p class="header-subtitle">Manage your collaborations and campaigns</p>
        </div>
        <div class="action-buttons">
          <button @click="$router.push('/influencer/profile')" class="action-btn profile-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            Manage Profile
          </button>
          <button @click="$router.push('/influencer/requests')" class="action-btn requests-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
            </svg>
            View Requests
          </button>
          <button @click="$router.push('/influencer/campaigns')" class="action-btn browse-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
            Browse Campaigns
          </button>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="stats-panel dashboard-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-title">Pending Requests</div>
              <div class="stat-value">{{ stats.pendingRequests }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-title">Active Collaborations</div>
              <div class="stat-value">{{ stats.activeCollaborations }}</div>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <div class="stat-content">
              <div class="stat-title">Total Campaigns</div>
              <div class="stat-value">{{ stats.totalCampaigns }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Ad Requests -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>Recent Ad Requests</h2>
          <button @click="$router.push('/influencer/requests')" class="action-btn view-all-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            View All
          </button>
        </div>

        <div class="requests-grid" v-if="recentRequests.length">
          <div v-for="request in recentRequests" 
               :key="request.id" 
               class="request-card">
            <div class="request-header">
              <h3>{{ getCampaignDetails(request.campaign_id).title }}</h3>
              <span :class="['status-badge', request.status]">
                {{ request.status }}
              </span>
            </div>
            
            <div class="request-body">
              <p>{{ request.details || 'No additional details' }}</p>
              <div class="request-meta">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                {{ formatDate(request.created_at) }}
              </div>
            </div>

            <div class="request-actions" v-if="request.status === 'pending'">
              <button 
                @click="handleRequest(request.id, 'accept')"
                class="action-btn accept-btn"
                :disabled="processingId === request.id"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 13l4 4L19 7"/>
                </svg>
                {{ processingId === request.id ? 'Processing...' : 'Accept' }}
              </button>
              <button 
                @click="handleRequest(request.id, 'reject')"
                class="action-btn reject-btn"
                :disabled="processingId === request.id"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 18L18 6M6 6l12 12"/>
                </svg>
                {{ processingId === request.id ? 'Processing...' : 'Reject' }}
              </button>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          <p>No recent ad requests</p>
        </div>
      </div>

      <!-- Available Campaigns -->
      <div class="dashboard-section">
        <div class="section-header">
          <h2>Available Campaigns</h2>
          <button @click="$router.push('/influencer/campaigns')" class="action-btn view-all-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 15l6 6m-6-6v4.8m0-4.8h4.8M9 9L3 3m6 0v4.8M9 3H4.2M21 3h-4.8m4.8 0v4.8M3 21h4.8m-4.8 0v-4.8"/>
            </svg>
            Browse All
          </button>
        </div>

        <div class="campaigns-grid" v-if="availableCampaigns.length">
          <div v-for="campaign in availableCampaigns" 
               :key="campaign.id" 
               class="campaign-card">
            <h3>{{ campaign.title }}</h3>
            <div class="campaign-details">
              <div class="detail-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>${{ campaign.budget }}</span>
              </div>
              <div class="detail-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
                <span>{{ campaign.category }}</span>
              </div>
            </div>
            <p>{{ campaign.description }}</p>
            <button 
              @click="viewCampaignDetails(campaign)"
              class="action-btn view-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                <path d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
              </svg>
              View Details
            </button>
          </div>
        </div>
        <div v-else class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <p>No available campaigns</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'InfluencerDashboard',
  data() {
    return {
      stats: {
        pendingRequests: 0,
        activeCollaborations: 0,
        totalCampaigns: 0
      },
      recentRequests: [],
      availableCampaigns: [],
      campaignDetails: {},
      loading: true,
      error: null,
      processingId: null
    }
  },
  created() {
    this.fetchDashboardData()
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
    async fetchDashboardData() {
      try {
        this.loading = true
        await Promise.all([
          this.fetchAdRequests(),
          this.fetchAvailableCampaigns()
        ])
        this.updateStats()
      } catch (err) {
        console.error('Error fetching dashboard data:', err)
        this.error = 'Failed to load dashboard data'
      } finally {
        this.loading = false
      }
    },
    async fetchAdRequests() {
      const response = await axios.get('/influencer_ad_requests')
      this.recentRequests = response.data
      
      // Fetch campaign details for each request
      const campaignIds = [...new Set(this.recentRequests.map(r => r.campaign_id))]
      await this.fetchCampaignDetails(campaignIds)
    },
    async fetchAvailableCampaigns() {
      const response = await axios.get('/search_campaigns')
      this.availableCampaigns = response.data
    },
    async fetchCampaignDetails(campaignIds) {
      for (const id of campaignIds) {
        try {
          const response = await axios.get(`/campaigns/${id}`)
          this.$set(this.campaignDetails, id, response.data)
        } catch (err) {
          console.error(`Error fetching campaign ${id}:`, err)
        }
      }
    },
    getCampaignDetails(campaignId) {
      const campaign = this.campaignDetails[campaignId]
      if (!campaign) {
        // Return dummy data while loading
        return {
          title: 'Summer Collection Campaign',
          budget: '5,000',
          category: 'Fashion & Lifestyle',
          description: 'Showcase our latest summer collection through creative content and engaging posts.',
          dummyData: true
        }
      }
      return campaign
    },

    updateStats() {
      this.stats = {
        pendingRequests: this.recentRequests.filter(r => r.status === 'pending').length,
        activeCollaborations: this.recentRequests.filter(r => r.status === 'accepted').length,
        totalCampaigns: this.recentRequests.length
      }
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
        const request = this.recentRequests.find(r => r.id === requestId)
        if (request) {
          request.status = action === 'accept' ? 'accepted' : 'rejected'
        }
        
        this.updateStats()
        alert(`Request ${action}ed successfully`)
      } catch (err) {
        console.error('Error handling request:', err)
        alert(`Failed to ${action} request`)
      } finally {
        this.processingId = null
      }
    },
    viewCampaignDetails(campaign) {
      this.$router.push(`/influencer/campaigns/${campaign.id}`)
    }
  }
}
</script>
<style scoped>
.influencer-dashboard {
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

/* Header Styles */
.dashboard-header {
  margin-bottom: 2rem;
}

.header-content {
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

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Stats Panel */
.stats-panel {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
}

.stat-icon {
  width: 48px;
  height: 48px;
  color: #6366f1;
}

.stat-content {
  flex: 1;
}

.stat-title {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: #fff;
  font-size: 2rem;
  font-weight: 600;
}

/* Dashboard Sections */
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: #fff;
  font-size: 1.5rem;
  margin: 0;
}

/* Request Cards */
.requests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.request-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.request-card h3 {
  color: #fff;
  margin: 0;
  font-size: 1.25rem;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
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

.request-body {
  color: #94a3b8;
  margin-bottom: 1.5rem;
}

.request-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #6366f1;
  font-size: 0.875rem;
}

.request-meta svg {
  width: 16px;
  height: 16px;
}

.request-actions {
  display: flex;
  gap: 1rem;
}

/* Campaign Cards */
.campaigns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

.campaign-card {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 20px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.campaign-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #6366f1, #818cf8);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.campaign-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}

.campaign-card:hover::before {
  opacity: 1;
}

.campaign-card h3 {
  color: #fff;
  margin: 0 0 1.25rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.4;
}

.campaign-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  color: #94a3b8;
  font-size: 0.9rem;
}

.detail-item svg {
  width: 18px;
  height: 18px;
  color: #6366f1;
}

.campaign-card p {
  color: #94a3b8;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0 0 1.5rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.campaign-card .view-btn {
  width: 100%;
  justify-content: center;
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
  font-weight: 500;
  padding: 0.75rem;
}

.campaign-card .view-btn:hover {
  background: rgba(99, 102, 241, 0.2);
  transform: translateY(-2px);
}

@media (max-width: 640px) {
  .campaigns-grid {
    grid-template-columns: 1fr;
  }
  
  .campaign-details {
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .detail-item {
    width: 100%;
    justify-content: center;
  }
}

/* Buttons */
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

.profile-btn {
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
}

.requests-btn {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
}

.browse-btn {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
}

.accept-btn {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
}

.reject-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

.view-btn {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
}

.view-all-btn {
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  color: #94a3b8;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #6366f1;
  opacity: 0.5;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.1rem;
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-content {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.75rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-icon {
    width: 36px;
    height: 36px;
  }

  .stat-value {
    font-size: 1.5rem;
  }

  .request-header {
    flex-direction: column;
    gap: 0.75rem;
  }

  .status-badge {
    align-self: flex-start;
  }
}
</style>