<template>
  <div class="admin-dashboard">
    <!-- Background Elements -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="content-wrapper">
      <h1>Admin Dashboard</h1>

      <!-- Loading & Error States -->
      <div v-if="loading" class="loading">
        Loading dashboard data...
      </div>
      
      <div v-if="error" class="error">
        {{ error }}
      </div>

      <!-- Main Dashboard Content -->
      <div v-if="!loading && !error">
        <!-- Statistics Overview -->
        <StatisticsPanel 
          :stats="dashboardStats" 
          class="dashboard-section" 
        />

        <!-- Sponsor Approvals section -->
        <SponsorApprovalsPanel
          class="dashboard-section"
          @sponsor-approved="fetchDashboardData"
        />

        <!-- User Management section -->
        <UserManagementPanel 
          class="dashboard-section" 
        />

        <!-- Campaign Management section -->
        <CampaignManagementPanel 
          class="dashboard-section" 
        />

        <!-- Recent Activity section -->
        <RecentActivityPanel
          class="dashboard-section"
          :recentCampaigns="recentCampaigns"
          :recentAdRequests="recentAdRequests"
        />

        <!-- Additional Sections -->
        <div class="dashboard-sections">
          <!-- Future sections will be added here -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import StatisticsPanel from './components/StatisticsPanel.vue'
import SponsorApprovalsPanel from './components/SponsorApprovals.vue'
import UserManagementPanel from './components/UserManagement.vue'
import CampaignManagementPanel from './components/CampaignManagement.vue'
import RecentActivityPanel from './components/RecentActivity.vue'


export default {
  name: 'AdminDashboard',
  components: {
    StatisticsPanel,
    SponsorApprovalsPanel,
    UserManagementPanel,
    CampaignManagementPanel,
    RecentActivityPanel
  },
  data() {
    return {
      dashboardStats: null,
      recentCampaigns: [],
      recentAdRequests: [],
      loading: true,
      error: null
    }
  },
  async created() {
    await this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get('/admin/dashboard')
        this.dashboardStats = response.data.statistics
        this.recentCampaigns = response.data.recent_campaigns
        this.recentAdRequests = response.data.recent_ad_requests
        this.loading = false
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to load dashboard data'
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
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
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  color: white;
  font-size: 2rem;
  margin-bottom: 2rem;
  text-align: center;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.dashboard-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
}

.dashboard-section:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.dashboard-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.section-placeholder {
  padding: 1.5rem;
  border: 1px dashed rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  text-align: center;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.02);
}

.loading, .error {
  text-align: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  color: #94a3b8;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.error {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.2);
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }

  h1 {
    font-size: 1.75rem;
  }

  .dashboard-section {
    padding: 1rem;
  }

  .dashboard-sections {
    grid-template-columns: 1fr;
  }
}
</style>