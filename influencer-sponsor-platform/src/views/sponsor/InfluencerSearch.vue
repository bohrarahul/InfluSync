  <template>
    <div class="influencer-search">
      <!-- Animated background circles -->
      <div class="dashboard-bg">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        <div class="circle circle-3"></div>
      </div>

      <div class="page-content">
        <h1>Find Influencers</h1>

        <!-- Search and Filters -->
        <div class="search-section">
          <div class="filters">
            <div class="filter-group">
              <label>Category</label>
              <div class="input-with-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                </svg>
                <input 
                  v-model.trim="filters.category" 
                  type="text"
                  placeholder="e.g., Fashion, Tech, Lifestyle"
                >
              </div>
            </div>

            <div class="filter-group">
              <label>Niche</label>
              <div class="input-with-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                <input 
                  v-model.trim="filters.niche" 
                  type="text"
                  placeholder="Specific niche"
                >
              </div>
            </div>

            <div class="filter-group">
              <label>Minimum Reach</label>
              <div class="input-with-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
                <input 
                  v-model.number="filters.min_reach" 
                  type="number"
                  placeholder="Minimum followers"
                >
              </div>
            </div>

            <div class="button-group">
              <button @click="searchInfluencers" class="search-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
                Search
              </button>

              <button @click="clearFilters" class="clear-btn">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M6 18L18 6M6 6l12 12"/>
                </svg>
                Clear Filters
              </button>
            </div>
          </div>
        </div>

        <!-- Loading & Error States -->
        <div v-if="loading" class="loading">
          <svg class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
          </svg>
          Searching influencers...
        </div>
        
        <div v-if="error" class="error-message">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="error-icon">
            <path d="M12 8v5M12 16h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ error }}
        </div>

        <!-- Search Summary -->
        <div class="search-summary" v-if="!loading && !error">
          <p>Found {{ influencers.length }} influencer(s)</p>
        </div>

        <!-- Influencers Grid -->
        <div v-if="!loading && influencers.length" class="influencers-grid">
          <div v-for="influencer in influencers" 
              :key="influencer.id" 
              class="influencer-card">
            <div class="influencer-info">
              <h3>{{ influencer.name }}</h3>
              <div class="stats">
                <div class="stat">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/>
                  </svg>
                  <div class="stat-content">
                    <span class="stat-label">Category</span>
                    <span class="stat-value">{{ influencer.category }}</span>
                  </div>
                </div>
                <div class="stat">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                  </svg>
                  <div class="stat-content">
                    <span class="stat-label">Niche</span>
                    <span class="stat-value">{{ influencer.niche }}</span>
                  </div>
                </div>
                <div class="stat">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                  </svg>
                  <div class="stat-content">
                    <span class="stat-label">Reach</span>
                    <span class="stat-value">{{ formatNumber(influencer.reach) }}</span>
                  </div>
                </div>
              </div>
              <p class="bio">{{ influencer.bio || 'No bio provided' }}</p>
            </div>

            <!-- Campaign Selection for Ad Request -->
            <div class="request-section">
              <select v-model="selectedCampaigns[influencer.id]" class="campaign-select">
                <option value="">Select a campaign</option>
                <option v-for="campaign in activeCampaigns" 
                        :key="campaign.id" 
                        :value="campaign.id">
                  {{ campaign.title }}
                </option>
              </select>

              <button 
                @click="sendRequest(influencer.id)"
                :disabled="!selectedCampaigns[influencer.id] || isRequesting === influencer.id"
                class="request-btn"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
                </svg>
                {{ isRequesting === influencer.id ? 'Sending...' : 'Send Ad Request' }}
              </button>
            </div>
          </div>
        </div>

        <!-- No Results Message -->
        <div v-if="!loading && !influencers.length" class="no-results">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
          </svg>
          <p>No influencers found matching your criteria</p>
        </div>
      </div>
    </div>
  </template>

  <script>
  import axios from 'axios'

  export default {
    name: 'InfluencerSearch',
    data() {
      return {
        influencers: [],
        activeCampaigns: [],
        loading: false,
        error: null,
        isRequesting: null,
        selectedCampaigns: {},
        filters: {
          category: '',
          niche: '',
          min_reach: null
        }
      }
    },
    created() {
      this.fetchActiveCampaigns()
      this.searchInfluencers() // Initial search without filters
    },
    methods: {
      formatNumber(num) {
        return new Intl.NumberFormat().format(num)
      },

      async fetchActiveCampaigns() {
        try {
          const response = await axios.get('/campaigns')
          this.activeCampaigns = response.data.filter(c => c.status === 'active')
        } catch (err) {
          console.error('Error fetching campaigns:', err)
          this.error = 'Failed to load your campaigns'
        }
      },

      async searchInfluencers() {
        try {
          this.loading = true
          const params = {}
          if (this.filters.category) params.category = this.filters.category
          if (this.filters.niche) params.niche = this.filters.niche
          if (this.filters.min_reach) params.min_reach = this.filters.min_reach

          const response = await axios.get('/search_influencers', { params })
          this.influencers = response.data
          this.error = null
        } catch (err) {
          console.error('Error searching influencers:', err)
          this.error = 'Failed to search influencers'
        } finally {
          this.loading = false
        }
      },

      clearFilters() {
        this.filters = {
          category: '',
          niche: '',
          min_reach: null
        }
        this.searchInfluencers()
      },

      async sendRequest(influencerId) {
        const campaignId = this.selectedCampaigns[influencerId]
        if (!campaignId) {
          alert('Please select a campaign first')
          return
        }

        try {
          this.isRequesting = influencerId
          await axios.post(`/send_ad_request/${influencerId}`, {
            campaign_id: campaignId,
            details: 'Interested in collaboration'
          })
          alert('Ad request sent successfully!')
          this.selectedCampaigns[influencerId] = '' // Reset selection
        } catch (err) {
          console.error('Error sending request:', err)
          alert('Failed to send request: ' + (err.response?.data?.message || err.message))
        } finally {
          this.isRequesting = null
        }
      }
    }
  }
  </script>

  <style scoped>
  .influencer-search {
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

  /* Page Content */
  .page-content {
    position: relative;
    z-index: 2;
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 2rem;
    background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
  }

  /* Search Section */
  .search-section {
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
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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

  .input-with-icon {
    position: relative;
  }

  .input-with-icon svg {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    width: 20px;
    height: 20px;
    color: #6366f1;
  }

  .input-with-icon input {
    width: 100%;
    padding: 0.875rem 1rem 0.875rem 3rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: white;
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  .input-with-icon input:hover {
    background: rgba(255, 255, 255, 0.08);
  }

  .input-with-icon input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
  }

  .input-with-icon input:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
    background: rgba(255, 255, 255, 0.08);
  }

  .button-group {
    display: flex;
    gap: 1rem;
  }

  .search-btn,
  .clear-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    border-radius: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .search-btn {
    background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
    color: white;
    border: none;
  }

  .clear-btn {
    background: rgba(255, 255, 255, 0.05);
    color: #94a3b8;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .search-btn:hover,
  .clear-btn:hover {
    transform: translateY(-2px);
  }

  .search-btn svg,
  .clear-btn svg {
    width: 20px;
    height: 20px;
  }

  /* Search Summary */
  .search-summary {
    color: #94a3b8;
    text-align: center;
    margin-bottom: 2rem;
  }

  /* Influencers Grid */
  .influencers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .influencer-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .influencer-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
      rgba(255, 255, 255, 0) 0%,
      rgba(255, 255, 255, 0.1) 50%,
      rgba(255, 255, 255, 0) 100%
    );
    transition: transform 0.3s ease;
    transform: translateX(-100%);
  }

  .influencer-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  }

  .influencer-card:hover::before {
    transform: translateX(100%);
  }

  .influencer-card:hover {
    transform: translateY(-5px);
  }

  .influencer-info h3 {
    color: white;
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }

  .stats {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .stat {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .stat svg {
    width: 24px;
    height: 24px;
    color: #6366f1;
  }

  .stat-content {
    display: flex;
    flex-direction: column;
  }

  .stat-label {
    color: #94a3b8;
    font-size: 0.875rem;
  }

  .stat-value {
    color: white;
    font-weight: 500;
  }

  .bio {
    color: #94a3b8;
    line-height: 1.6;
    margin-bottom: 1.5rem;
  }

  /* Request Section */
  .request-section {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .campaign-select {
    width: 100%;
    padding: 0.875rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    color: white;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    -webkit-appearance: none;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%236366f1' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    background-size: 1.25rem;
    padding-right: 2.5rem;
  }

  .campaign-select:hover {
    background-color: rgba(255, 255, 255, 0.08);
  }

  .campaign-select option {
    background-color: #1e1b4b;
    color: white;
    padding: 0.5rem;
  }

  .campaign-select:focus {
    outline: none;
    border-color: rgba(99, 102, 241, 0.5);
    background: rgba(255, 255, 255, 0.08);
  }

  .request-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .request-btn:hover:not(:disabled) {
    transform: translateY(-2px);
  }

  .request-btn:disabled {
    background: rgba(255, 255, 255, 0.1);
    cursor: not-allowed;
  }

  .request-btn svg {
    width: 20px;
    height: 20px;
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

  .no-results {
    text-align: center;
    color: #94a3b8;
    padding: 3rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .no-results svg {
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

    h1 {
      font-size: 2rem;
    }

    .button-group {
      flex-direction: column;
    }

    .influencer-card {
      padding: 1.25rem;
    }
  }

  @media (max-width: 480px) {
    h1 {
      font-size: 1.75rem;
    }

    .filters {
      grid-template-columns: 1fr;
    }

    .stats {
      gap: 0.75rem;
    }
  }
  </style>