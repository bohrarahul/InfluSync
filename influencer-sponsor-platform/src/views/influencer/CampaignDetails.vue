<template>
  <div class="campaign-details">
    <!-- Loading & Error States -->
    <div v-if="loading" class="loading">Loading campaign details...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!loading && campaign" class="campaign-content">
      <!-- Back Button -->
      <div class="back-section">
        <button @click="$router.go(-1)" class="back-btn">
          ← Back to Campaigns
        </button>
      </div>

      <!-- Campaign Header -->
      <div class="header-section">
        <div class="title-section">
          <h1>{{ campaign.title }}</h1>
          <span class="campaign-budget">${{ campaign.budget }}</span>
        </div>
        <div class="meta-info">
          <span class="category">{{ campaign.category }}</span>
          <span class="duration">
            {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}
          </span>
        </div>
      </div>

      <!-- Campaign Description -->
      <div class="description-section">
        <h2>Campaign Description</h2>
        <p>{{ campaign.description }}</p>
      </div>

      <!-- Campaign Requirements & Details -->
      <div class="details-section">
        <div class="info-grid">
          <div class="info-card">
            <h3>Duration</h3>
            <p>{{ calculateDuration(campaign.start_date, campaign.end_date) }} days</p>
          </div>
          <div class="info-card">
            <h3>Category</h3>
            <p>{{ campaign.category }}</p>
          </div>
          <div class="info-card">
            <h3>Budget</h3>
            <p>${{ campaign.budget }}</p>
          </div>
          <div class="info-card">
            <h3>Status</h3>
            <p class="status">{{ campaign.status }}</p>
          </div>
        </div>
      </div>

      <!-- Sponsor Information -->
      <div class="sponsor-section">
        <h2>Sponsor Information</h2>
        <div class="sponsor-details" v-if="campaign.sponsor">
          <div class="detail-row">
            <strong>Company:</strong> 
            <span>{{ campaign.sponsor.company_name }}</span>
          </div>
          <div class="detail-row">
            <strong>Industry:</strong> 
            <span>{{ campaign.sponsor.industry }}</span>
          </div>
          
          <!-- Email Contact Section -->
          <div class="contact-section">
            <button 
              v-if="!showEmail"
              @click="showEmail = true"
              class="contact-btn"
            >
              Contact Sponsor
            </button>
            <div v-else class="email-details">
              <p>Sponsor Email: 
                <a :href="'mailto:' + campaign.sponsor.email">
                  {{ campaign.sponsor.email }}
                </a>
              </p>
              <div class="email-note">
                <i>Note: When contacting the sponsor, please reference the campaign title: "{{ campaign.title }}"</i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Save for Later Feature -->
      <div class="action-section">
        <button 
          @click="toggleSaved"
          class="save-btn"
          :class="{ 'saved': isSaved }"
        >
          {{ isSaved ? 'Saved ★' : 'Save for Later ☆' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CampaignDetails',
  data() {
    return {
      campaign: null,
      loading: true,
      error: null,
      showEmail: false,
      isSaved: false
    }
  },
  created() {
    this.fetchCampaignDetails()
    this.isSaved = localStorage.getItem(`saved_campaign_${this.$route.params.id}`) === 'true'
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    calculateDuration(startDate, endDate) {
      const start = new Date(startDate)
      const end = new Date(endDate)
      const diffTime = Math.abs(end - start)
      return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    },
    async fetchCampaignDetails() {
      try {
        this.loading = true
        const campaignId = this.$route.params.id
        
        const response = await axios.get(`/campaigns/${campaignId}`)
        this.campaign = response.data
        
        this.error = null
      } catch (err) {
        console.error('Error details:', err.response || err)
        this.error = err.response?.data?.message || 'Failed to load campaign details'
      } finally {
        this.loading = false
      }
    },
    toggleSaved() {
      this.isSaved = !this.isSaved
      if (this.isSaved) {
        localStorage.setItem(`saved_campaign_${this.campaign.id}`, 'true')
      } else {
        localStorage.removeItem(`saved_campaign_${this.campaign.id}`)
      }
    }
  }
}
</script>

<style scoped>
.campaign-details {
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

.campaign-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
}

.back-section {
  margin-bottom: 2rem;
}

.back-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
  cursor: pointer;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-5px);
}

.header-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.header-section:hover {
  border-color: rgba(255, 255, 255, 0.2);
}

.title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.title-section h1 {
  color: white;
  font-size: 2rem;
  margin: 0;
  flex-grow: 1;
}

.campaign-budget {
  font-size: 1.25rem;
  font-weight: 600;
  color: #10b981;
  padding: 0.5rem 1rem;
  background: rgba(16, 185, 129, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(16, 185, 129, 0.2);
  white-space: nowrap;
}

.meta-info {
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
}

.category {
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
  padding: 0.5rem 1rem;
  border-radius: 12px;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.duration {
  color: #94a3b8;
}

.description-section,
.details-section,
.sponsor-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 2rem;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.description-section:hover,
.details-section:hover,
.sponsor-section:hover {
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

h2 {
  color: white;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.description-section p {
  color: #94a3b8;
  line-height: 1.6;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.info-card:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.info-card h3 {
  color: #94a3b8;
  font-size: 1rem;
  margin-bottom: 0.75rem;
}

.info-card p {
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.sponsor-details {
  margin-top: 1.5rem;
}

.detail-row {
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
  color: #94a3b8;
}

.detail-row strong {
  color: white;
}

.contact-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.contact-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.contact-btn:hover {
  transform: translateY(-2px);
}

.email-details {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin-top: 1rem;
  color: #94a3b8;
}

.email-details a {
  color: #818cf8;
  text-decoration: none;
  transition: color 0.3s ease;
}

.email-details a:hover {
  color: #6366f1;
}

.email-note {
  margin-top: 1rem;
  color: #64748b;
  font-size: 0.9rem;
}

.save-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  color: #94a3b8;
  transition: all 0.3s ease;
}

.save-btn.saved {
  background: rgba(250, 204, 21, 0.1);
  border-color: rgba(250, 204, 21, 0.2);
  color: #facc15;
}

.save-btn:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.1);
}

.save-btn.saved:hover {
  background: rgba(250, 204, 21, 0.2);
}

.loading, .error-message {
  text-align: center;
  padding: 3rem;
  color: #94a3b8;
}

.error-message {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 12px;
}

@media (max-width: 768px) {
  .campaign-details {
    padding: 1rem;
  }

  .title-section {
    flex-wrap: wrap;
    gap: 1rem;
  }

  .title-section h1 {
    font-size: 1.75rem;
  }

  .meta-info {
    flex-direction: column;
    gap: 1rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>