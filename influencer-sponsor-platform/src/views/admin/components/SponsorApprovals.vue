<template>
  <div class="sponsor-approvals">
    <h2>Pending Sponsor Approvals</h2>

    <!-- Loading and Error States -->
    <div v-if="loading" class="loading">Loading sponsor approvals...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <!-- No Pending Approvals Message -->
    <div v-if="!loading && !pendingSponsors.length" class="no-data">
      <p>No pending sponsor approvals</p>
      <p>New sponsor applications will appear here for review</p>
    </div>

    <!-- Sponsors List -->
    <div v-if="pendingSponsors.length" class="sponsors-list">
      <div v-for="sponsor in pendingSponsors" 
           :key="sponsor.id" 
           class="sponsor-card">
        <div class="sponsor-info">
          <h3>{{ sponsor.company_name || 'Company Name Not Set' }}</h3>
          <div class="sponsor-details">
            <p>
              <strong>Industry:</strong>
              <span>{{ sponsor.industry || 'Not specified' }}</span>
            </p>
            <p>
              <strong>Budget:</strong>
              <span>${{ sponsor.budget || 'Not specified' }}</span>
            </p>
            <p>
              <strong>Description:</strong>
              <span>{{ sponsor.description || 'No description provided' }}</span>
            </p>
          </div>
        </div>

        <div class="sponsor-actions">
          <button 
            @click="approveSponsor(sponsor.id)"
            :disabled="processingId === sponsor.id"
            class="approve-btn"
          >
            {{ processingId === sponsor.id ? 'Approving...' : 'Approve' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'SponsorApprovalsPanel',
  data() {
    return {
      pendingSponsors: [],
      loading: true,
      error: null,
      processingId: null
    }
  },
  created() {
    this.fetchPendingSponsors()
  },
  methods: {
    async fetchPendingSponsors() {
      try {
        this.loading = true
        // Log the request
        console.log('Fetching pending sponsors...')
        
        const response = await axios.get('/admin/approve_sponsors')
        console.log('Response:', response.data) // Log successful response
        
        this.pendingSponsors = response.data.unapproved_sponsors
        this.error = null
      } catch (err) {
        // Log the detailed error
        console.error('Error fetching sponsors:', err)
        console.error('Error response:', err.response)
        
        this.error = err.response?.data?.message || 'Failed to fetch pending sponsors'
      } finally {
        this.loading = false
      }
    },
    async approveSponsor(sponsorId) {
      try {
        this.processingId = sponsorId
        await axios.post(`/admin/approve_sponsors/${sponsorId}`)
        // Remove approved sponsor from list
        this.pendingSponsors = this.pendingSponsors.filter(s => s.id !== sponsorId)
        this.$emit('sponsor-approved') // Emit event to refresh dashboard stats if needed
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to approve sponsor'
      } finally {
        this.processingId = null
      }
    }
  }
}
</script>

<style scoped>
.sponsor-approvals {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
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

.sponsors-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.sponsor-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  transition: all 0.3s ease;
}

.sponsor-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.sponsor-info {
  flex: 1;
}

.sponsor-info h3 {
  color: #e2e8f0;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.sponsor-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.sponsor-details p {
  color: #94a3b8;
  margin: 0;
  line-height: 1.5;
}

.sponsor-details strong {
  color: #e2e8f0;
  font-weight: 500;
  display: inline-block;
  min-width: 100px;
}

.sponsor-actions {
  display: flex;
  gap: 1rem;
}

.approve-btn {
  padding: 0.75rem 1.5rem;
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
}

.approve-btn:hover {
  background: rgba(16, 185, 129, 0.2);
  transform: translateY(-2px);
}

.approve-btn:disabled {
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
  border-color: rgba(148, 163, 184, 0.2);
  cursor: not-allowed;
  transform: none;
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
  border-radius: 12px;
}

.no-data {
  color: #64748b;
  font-style: italic;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
}

@media (max-width: 768px) {
  .sponsor-approvals {
    padding: 1rem;
  }

  .sponsor-card {
    flex-direction: column;
    padding: 1.25rem;
  }

  .sponsor-actions {
    width: 100%;
  }

  .approve-btn {
    width: 100%;
  }

  .sponsor-details strong {
    min-width: 80px;
  }
}
</style>