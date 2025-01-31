<template>
  <div class="sponsor-dashboard">
    <!-- Animated background circles -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="dashboard-content">
      <div class="dashboard-header">
        <h1>Sponsor Dashboard</h1>
        <p class="header-subtitle">Welcome back, {{ profile?.company_name }}</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading">
        <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
        </svg>
        Loading dashboard...
      </div>

      <div v-if="error" class="error-message">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
          <path d="M12 8v5M12 16h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        {{ error }}
      </div>

      <!-- Profile Completion Alert -->
      <div v-if="!isProfileComplete" class="alert">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="alert-icon">
          <path d="M12 8v5M12 16h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        Please complete your profile to access all features
      </div>

      <div class="dashboard-grid">
        <!-- Quick Stats -->
        <div class="dashboard-section stats-panel">
          <h2>Overview</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-title">Active Campaigns</div>
                <div class="stat-value">
                  {{ campaigns.filter(c => c.status === 'active').length }}
                </div>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l4 4L7 17l-4-4L13 3z"/>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-title">Pending Requests</div>
                <div class="stat-value">
                  {{ adRequests.filter(r => r.status === 'pending').length }}
                </div>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 20V10M18 20V4M6 20v-4"/>
                </svg>
              </div>
              <div class="stat-content">
                <div class="stat-title">Total Campaigns</div>
                <div class="stat-value">{{ campaigns.length }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Summary -->
        <div class="dashboard-section profile-panel">
          <h2>Profile</h2>
          <SponsorProfile 
            :profile="profile"
            @profile-updated="fetchProfile"
          />
        </div>

        <!-- Quick Actions -->
        <div class="dashboard-section actions-panel">
          <h2>Quick Actions</h2>
          <div class="action-buttons">
            <div class="action-group">
              <h3>Campaign Management</h3>
              <button @click="$router.push('/sponsor/campaigns/new')" class="action-btn create-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 5v14M5 12h14"/>
                </svg>
                Create Campaign
              </button>
              <button @click="$router.push('/sponsor/campaigns')" class="action-btn manage-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 20V10M18 20V4M6 20v-4"/>
                </svg>
                Manage Campaigns
              </button>
              <button @click="$router.push('/sponsor/export')" class="action-btn export-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                </svg>
                Export Campaign Data
              </button>
            </div>

            <div class="action-group">
              <h3>Collaboration</h3>
              <button @click="$router.push('/sponsor/influencers')" class="action-btn find-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                Find Influencers
              </button>
              <button @click="$router.push('/sponsor/requests')" class="action-btn view-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                </svg>
                View Requests
              </button>
            </div>
          </div>
        </div>

        <!-- Monthly Report Preview -->
        <div class="dashboard-section report-panel">
          <div class="section-header">
            <h2>Monthly Report</h2>
            <span class="report-date">{{ getCurrentMonth() }}</span>
          </div>
          <div class="report-summary">
            <div class="report-stat">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="stat-content">
                <span class="label">Budget Used</span>
                <span class="value">${{ calculateBudgetUsed() }}</span>
              </div>
            </div>
            <div class="report-stat">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
              </div>
              <div class="stat-content">
                <span class="label">Active Collaborations</span>
                <span class="value">{{ getActiveCollaborations() }}</span>
              </div>
            </div>
            <div class="report-stat">
              <div class="stat-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
              </div>
              <div class="stat-content">
                <span class="label">Response Rate</span>
                <span class="value">{{ calculateResponseRate() }}%</span>
              </div>
            </div>
          </div>
          <p class="report-note">
            Monthly detailed report will be sent to your email on the 1st of each month.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SponsorProfile from './components/SponsorProfile.vue'

export default {
 name: 'SponsorDashboard',
 components: {
   SponsorProfile
 },
 data() {
   return {
     profile: null,
     campaigns: [],
     adRequests: [],
     loading: true,
     error: null,
     monthlyStats: {
       budgetUsed: 0,
       activeCollaborations: 0,
       responseRate: 0
     }
   }
 },
 computed: {
   isProfileComplete() {
     if (!this.profile) return false
     return !!(
       this.profile.company_name &&
       this.profile.industry &&
       this.profile.description
     )
   }
 },
 created() {
   this.fetchDashboardData()
 },
 methods: {
   async fetchDashboardData() {
     try {
       this.loading = true
       await Promise.all([
         this.fetchProfile(),
         this.fetchCampaigns(),
         this.fetchAdRequests()
       ])
       this.updateMonthlyStats()
       this.error = null
     } catch (err) {
       console.error('Error fetching dashboard data:', err)
       this.error = 'Failed to load dashboard data'
     } finally {
       this.loading = false
     }
   },
   async fetchProfile() {
     const response = await axios.get('/profile')
     this.profile = response.data
   },
   async fetchCampaigns() {
     const response = await axios.get('/campaigns')
     this.campaigns = response.data
   },
   async fetchAdRequests() {
     const response = await axios.get('/ad_requests')
     this.adRequests = response.data
   },
   getCurrentMonth() {
     return new Date().toLocaleString('default', { month: 'long', year: 'numeric' })
   },
   updateMonthlyStats() {
     // Calculate budget used
     const totalBudget = this.campaigns.reduce((sum, campaign) => {
       return sum + (campaign.budget || 0)
     }, 0)
     this.monthlyStats.budgetUsed = Math.round(totalBudget * 0.7) // 70% usage simulation

     // Calculate active collaborations
     this.monthlyStats.activeCollaborations = this.adRequests.filter(
       request => request.status === 'accepted'
     ).length

     // Calculate response rate
     const totalRequests = this.adRequests.length
     const respondedRequests = this.adRequests.filter(
       request => request.status !== 'pending'
     ).length
     this.monthlyStats.responseRate = totalRequests ? 
       Math.round((respondedRequests / totalRequests) * 100) : 0
   },
   calculateBudgetUsed() {
     return this.monthlyStats.budgetUsed.toLocaleString()
   },
   getActiveCollaborations() {
     return this.monthlyStats.activeCollaborations
   },
   calculateResponseRate() {
     return this.monthlyStats.responseRate
   }
 }
}
</script>
<style scoped>
.sponsor-dashboard {
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

/* Grid Layout */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Section Styling */
.dashboard-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease;
}

.dashboard-section:hover {
  transform: translateY(-5px);
}

.dashboard-section h2 {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

/* Stats Panel */
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

/* Action Buttons */
.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.action-group h3 {
  color: #94a3b8;
  font-size: 1rem;
  margin-bottom: 1rem;
}

.action-btn {
  width: 100%;
  padding: 0.875rem 1rem;
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 0.75rem;
}

.action-btn svg {
  width: 20px;
  height: 20px;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.create-btn svg { color: #10b981; }
.manage-btn svg { color: #6366f1; }
.export-btn svg { color: #8b5cf6; }
.find-btn svg { color: #3b82f6; }
.view-btn svg { color: #ec4899; }

/* Report Panel */
.report-panel {
  grid-column: 1 / -1;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.report-date {
  color: #94a3b8;
  font-size: 0.9rem;
}

.report-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.report-stat {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.report-stat .stat-content {
  display: flex;
  flex-direction: column;
}

.report-stat .label {
  color: #94a3b8;
  font-size: 0.9rem;
}

.report-stat .value {
  color: #fff;
  font-size: 1.25rem;
  font-weight: 600;
}

.report-note {
  color: #94a3b8;
  text-align: center;
  font-style: italic;
  font-size: 0.9rem;
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

.error-message, .alert {
  background: rgba(220, 38, 38, 0.1);
  color: #ef4444;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 1px solid rgba(220, 38, 38, 0.2);
}

.alert {
  background: rgba(234, 179, 8, 0.1);
  color: #eab308;
  border-color: rgba(234, 179, 8, 0.2);
}

.error-icon, .alert-icon {
  width: 20px;
  height: 20px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-content {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 2rem;
  }

  .stats-grid, .report-summary {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .dashboard-section {
    padding: 1.25rem;
  }
}

@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.75rem;
  }

  .stat-card, .report-stat {
    padding: 1rem;
  }

  .stat-icon, .report-stat .stat-icon {
    width: 32px;
    height: 32px;
  }

  .stat-value {
    font-size: 1.25rem;
  }
}
</style>