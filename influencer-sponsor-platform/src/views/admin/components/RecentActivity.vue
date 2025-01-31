<template>
  <div class="recent-activity">
    <h2>Recent Activity</h2>

    <div class="activity-sections">
      <!-- Recent Campaigns -->
      <div class="activity-section">
        <h3>Recent Campaigns</h3>
        <div v-if="recentCampaigns.length" class="activity-list">
          <div v-for="campaign in recentCampaigns"
               :key="campaign.id"
               class="activity-item">
            <div class="activity-content">
              <strong>{{ campaign.title }}</strong>
              <span class="status-badge" :class="campaign.status">
                {{ campaign.status }}
              </span>
            </div>
            <div class="activity-meta">
              Sponsor ID: {{ campaign.sponsor_id }}
            </div>
          </div>
        </div>
        <div v-else class="no-data">
          <p>No recent campaigns</p>
          <p>New campaigns will appear here</p>
        </div>
      </div>

      <!-- Recent Ad Requests -->
      <div class="activity-section">
        <h3>Recent Ad Requests</h3>
        <div v-if="recentAdRequests.length" class="activity-list">
          <div v-for="request in recentAdRequests"
               :key="request.id"
               class="activity-item">
            <div class="activity-content">
              <strong>Campaign ID: {{ request.campaign_id }}</strong>
              <span class="status-badge" :class="request.status">
                {{ request.status }}
              </span>
            </div>
            <div class="activity-meta">
              Influencer ID: {{ request.influencer_id }}
            </div>
          </div>
        </div>
        <div v-else class="no-data">
          <p>No recent ad requests</p>
          <p>New requests will appear here</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RecentActivityPanel',
  props: {
    recentCampaigns: {
      type: Array,
      default: () => []
    },
    recentAdRequests: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>
.recent-activity {
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

h3 {
  color: #e2e8f0;
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.activity-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.activity-section {
  background: rgba(255, 255, 255, 0.02);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.25rem;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.activity-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1rem;
  transition: all 0.3s ease;
}

.activity-item:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.activity-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.activity-content strong {
  color: #e2e8f0;
  font-size: 0.95rem;
}

.activity-meta {
  font-size: 0.9rem;
  color: #94a3b8;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
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

.status-badge.completed {
  background: rgba(99, 102, 241, 0.1);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.no-data {
  text-align: center;
  color: #64748b;
  font-style: italic;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

@media (max-width: 768px) {
  .recent-activity {
    padding: 1rem;
  }

  .activity-sections {
    grid-template-columns: 1fr;
  }

  .activity-section {
    padding: 1rem;
  }

  .activity-item {
    padding: 0.875rem;
  }

  .status-badge {
    padding: 0.375rem 0.75rem;
    font-size: 0.8rem;
  }
}
</style>