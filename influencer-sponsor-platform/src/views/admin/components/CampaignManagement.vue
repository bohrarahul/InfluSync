<template>
  <div class="campaign-management">
    <h2>Campaign Management</h2>

    <!-- Filters -->
    <div class="filters">
      <select v-model="statusFilter" class="filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
        <option value="completed">Completed</option>
      </select>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="loading">Loading campaigns...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <!-- Campaigns Table -->
    <div class="campaigns-table-container" v-if="!loading && filteredCampaigns.length">
      <table class="campaigns-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Sponsor</th>
            <th>Budget</th>
            <th>Status</th>
            <th>Duration</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="campaign in filteredCampaigns" :key="campaign.id">
            <td>{{ campaign.title }}</td>
            <td>{{ campaign.sponsor_id }}</td>
            <td>${{ campaign.budget }}</td>
            <td>
              <span :class="['status-badge', campaign.status]">
                {{ campaign.status }}
              </span>
            </td>
            <td>
              {{ formatDate(campaign.start_date) }} - {{ formatDate(campaign.end_date) }}
            </td>
            <td>
              <button 
                @click="updateCampaignStatus(campaign.id, campaign.status === 'active' ? 'inactive' : 'active')"
                :disabled="processingId === campaign.id"
                :class="['toggle-btn', campaign.status === 'active' ? 'deactivate' : 'activate']"
              >
                {{ processingId === campaign.id ? 'Processing...' : 
                   campaign.status === 'active' ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No Campaigns Message -->
    <div v-if="!loading && !filteredCampaigns.length" class="no-data">
      <p>No campaigns found matching the selected filters</p>
      <p class="suggestion">Try adjusting your filters or check back later.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CampaignManagementPanel',
  data() {
    return {
      campaigns: [],
      loading: true,
      error: null,
      processingId: null,
      statusFilter: ''
    }
  },
  computed: {
    filteredCampaigns() {
      return this.campaigns.filter(campaign => {
        return !this.statusFilter || campaign.status === this.statusFilter
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
        const response = await axios.get('/admin/campaigns')
        this.campaigns = response.data
        this.error = null
      } catch (err) {
        console.error('Error fetching campaigns:', err)
        this.error = 'Failed to load campaigns'
      } finally {
        this.loading = false
      }
    },
    async updateCampaignStatus(campaignId, newStatus) {
      try {
        this.processingId = campaignId
        await axios.put(`/admin/campaigns/${campaignId}`, {
          status: newStatus
        })
        
        // Update local state
        const updatedCampaign = this.campaigns.find(c => c.id === campaignId)
        if (updatedCampaign) {
          updatedCampaign.status = newStatus
        }
        
        this.error = null
      } catch (err) {
        console.error('Error updating campaign status:', err)
        this.error = 'Failed to update campaign status'
      } finally {
        this.processingId = null
      }
    }
  }
}
</script>

<style scoped>
.campaign-management {
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

.filters {
  margin-bottom: 1.5rem;
}

.filter-select {
  width: 100%;
  max-width: 200px;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e2e8f0;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.filter-select:hover {
  background: rgba(255, 255, 255, 0.08);
}

.filter-select:focus {
  outline: none;
  border-color: rgba(99, 102, 241, 0.5);
}

.filter-select option {
  background: #1e1b4b;
  color: #e2e8f0;
  padding: 0.5rem;
}

.campaigns-table-container {
  overflow-x: auto;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.campaigns-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 0;
}

.campaigns-table th,
.campaigns-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: #94a3b8;
}

.campaigns-table th {
  background: rgba(255, 255, 255, 0.03);
  font-weight: 500;
  color: white;
  position: sticky;
  top: 0;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.campaigns-table tr:hover td {
  background: rgba(255, 255, 255, 0.03);
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
  display: inline-block;
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
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.toggle-btn {
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.toggle-btn.activate {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border-color: rgba(16, 185, 129, 0.2);
}

.toggle-btn.deactivate {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.2);
}

.toggle-btn:hover {
  transform: translateY(-2px);
}

.toggle-btn.activate:hover {
  background: rgba(16, 185, 129, 0.2);
}

.toggle-btn.deactivate:hover {
  background: rgba(239, 68, 68, 0.2);
}

.toggle-btn:disabled {
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
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
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

@media (max-width: 768px) {
  .campaign-management {
    padding: 1rem;
  }

  .campaigns-table td, 
  .campaigns-table th {
    padding: 0.75rem;
    font-size: 0.9rem;
  }

  .toggle-btn {
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }

  .status-badge {
    padding: 0.375rem 0.75rem;
    font-size: 0.8rem;
  }
}
</style>