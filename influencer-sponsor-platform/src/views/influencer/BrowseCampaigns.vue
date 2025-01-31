<script>
import axios from 'axios'

export default {
  name: 'BrowseCampaigns',
  data() {
    return {
      campaigns: [],
      loading: false,
      error: null,
      filters: {
        category: '',
        min_budget: null,
        start_date: '',
        end_date: ''
      },
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
      ]
    }
  },
  created() {
    this.fetchCampaigns()
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'TBD'
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      })
    },
    truncateText(text, length) {
      if (!text) return ''
      if (text.length <= length) return text
      return text.substring(0, length).trim() + '...'
    },
    async fetchCampaigns() {
      try {
        this.loading = true
        this.error = null

        const params = {}
        if (this.filters.category) params.category = this.filters.category
        if (this.filters.min_budget) params.min_budget = this.filters.min_budget
        if (this.filters.start_date) params.start_date = this.filters.start_date
        if (this.filters.end_date) params.end_date = this.filters.end_date

        const response = await axios.get('/search_campaigns', { params })
        this.campaigns = response.data.map(campaign => ({
          ...campaign,
          budget: new Intl.NumberFormat('en-US', {
            style: 'decimal',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
          }).format(campaign.budget)
        }))
      } catch (err) {
        console.error('Error fetching campaigns:', err)
        this.error = 'Failed to load campaigns. Please try again.'
      } finally {
        this.loading = false
      }
    },
    applyFilters() {
      this.fetchCampaigns()
    },
    clearFilters() {
      this.filters = {
        category: '',
        min_budget: null,
        start_date: '',
        end_date: ''
      }
      this.fetchCampaigns()
    },
    viewDetails(campaignId) {
      this.$router.push(`/influencer/campaigns/${campaignId}`)
    }
  }
}
</script>

<template>
  <div class="browse-campaigns">
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="browse-content">
      <h1 class="page-title">Browse Campaigns</h1>
      <p class="page-subtitle">Discover and apply to exciting brand collaborations</p>

      <div class="filters-section dashboard-section">
        <div class="filters">
          <div class="filter-group">
            <label>Category</label>
            <select v-model="filters.category" class="filter-input">
              <option value="">All Categories</option>
              <option v-for="category in categories" 
                      :key="category" 
                      :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label>Minimum Budget</label>
            <input 
              type="number" 
              v-model.number="filters.min_budget"
              placeholder="Enter minimum budget"
              class="filter-input">
          </div>

          <div class="filter-group">
            <label>Start Date After</label>
            <input 
              type="date" 
              v-model="filters.start_date"
              class="filter-input">
          </div>

          <div class="filter-group">
            <label>End Date Before</label>
            <input 
              type="date" 
              v-model="filters.end_date"
              class="filter-input">
          </div>

          <div class="filter-actions">
            <button @click="applyFilters" class="action-btn apply-btn">
              Apply Filters
            </button>
            <button @click="clearFilters" class="action-btn clear-btn">
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        Loading campaigns...
      </div>

      <div v-if="error" class="error-state">
        {{ error }}
      </div>

      <div v-if="!loading && !error" class="results-summary">
        Found {{ campaigns.length }} campaigns matching your criteria
      </div>

      <div v-if="!loading && campaigns.length" class="campaigns-grid">
        <div v-for="campaign in campaigns" 
             :key="campaign.id" 
             class="campaign-card dashboard-section">
          <div class="campaign-header">
            <h3>{{ campaign.title }}</h3>
            <span class="budget-tag">
              ${{ campaign.budget }}
            </span>
          </div>

          <div class="campaign-body">
            <div class="campaign-description">
              {{ truncateText(campaign.description, 150) }}
            </div>
            
            <div class="campaign-meta">
              <div class="meta-item">
                {{ campaign.category }}
              </div>
              <div class="meta-item">
                {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}
              </div>
            </div>
          </div>

          <div class="campaign-actions">
            <button 
              @click="viewDetails(campaign.id)" 
              class="action-btn view-btn">
              View Details
            </button>
          </div>
        </div>
      </div>

      <div v-if="!loading && !campaigns.length" class="empty-state">
        <p>No campaigns found matching your criteria.</p>
        <p class="suggestion">Try adjusting your filters or check back later for new opportunities.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.browse-campaigns {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  position: relative;
  overflow: hidden;
}

.browse-content {
  position: relative;
  z-index: 2;
  padding: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  text-align: center;
  color: #94a3b8;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.filters-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.filters-section:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
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
  font-weight: 500;
}

.filter-input {
  width: 100%;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.filter-input:hover {
  background: rgba(255, 255, 255, 0.08);
}

.filter-input:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.5);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
}


/* For WebKit browsers like Chrome and Safari */
.filter-input option {
  background: #0f172a !important; /* Slightly darker for options */
  color: #e2e8f0;
}

.filter-input:focus {
  outline: none;
  border-color: #6366f1;
  background: rgba(255, 255, 255, 0.08);
}

.filter-input::placeholder {
  color: #64748b;
}

.filter-actions {
  display: flex;
  gap: 1rem;
  align-self: flex-end;
}

.campaigns-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.campaign-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.campaign-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.05);
}

.campaign-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

.campaign-header h3 {
  color: #fff;
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.budget-tag {
  padding: 0.5rem 1rem;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 12px;
  color: #818cf8;
  font-size: 0.9rem;
  font-weight: 500;
}

.campaign-description {
  color: #94a3b8;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1.25rem;
}

.campaign-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.meta-item {
  color: #94a3b8;
  font-size: 0.9rem;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  color: #94a3b8;
}

.error-state {
  color: #f87171;
}

.suggestion {
  color: #64748b;
  font-size: 0.9rem;
  margin-top: 0.75rem;
}

.results-summary {
  color: #94a3b8;
  text-align: center;
  margin: 1.5rem 0;
  font-size: 1.1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
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

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.apply-btn {
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
}

.clear-btn {
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
}

.view-btn {
  width: 100%;
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
}

.view-btn:hover {
  background: rgba(99, 102, 241, 0.2);
}

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

@media (max-width: 768px) {
  .browse-content {
    padding: 1rem;
  }

  .page-title {
    font-size: 2rem;
  }

  .filters {
    grid-template-columns: 1fr;
  }

  .filter-actions {
    flex-direction: column;
    width: 100%;
  }

  .action-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.75rem;
  }

  .campaign-header {
    flex-direction: column;
    gap: 0.75rem;
  }

  .budget-tag {
    align-self: flex-start;
  }

  .campaign-meta {
    gap: 1rem;
  }
}


</style>