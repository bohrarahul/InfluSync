<template>
  <div class="statistics-panel">
    <h2>Platform Overview</h2>
    <div class="stats-grid">
      <!-- Users Statistics -->
      <div class="stat-card">
        <div class="stat-title">Users</div>
        <div class="stat-numbers">
          <div>Total: {{ stats?.total_users || 0 }}</div>
          <div>Active: {{ stats?.active_users || 0 }}</div>
        </div>
      </div>

      <!-- Role Statistics -->
      <div class="stat-card">
        <div class="stat-title">User Types</div>
        <div class="stat-numbers">
          <div>Sponsors: {{ stats?.total_sponsors || 0 }}</div>
          <div>Influencers: {{ stats?.total_influencers || 0 }}</div>
        </div>
      </div>

      <!-- Campaign Statistics -->
      <div class="stat-card">
        <div class="stat-title">Campaigns</div>
        <div class="stat-numbers">
          <div>Total: {{ stats?.total_campaigns || 0 }}</div>
          <div>Active: {{ stats?.active_campaigns || 0 }}</div>
        </div>
      </div>

      <!-- Ad Request Statistics -->
      <div class="stat-card">
        <div class="stat-title">Ad Requests</div>
        <div class="stat-numbers">
          <div>Total: {{ stats?.total_ad_requests || 0 }}</div>
          <div>Pending: {{ stats?.pending_ad_requests || 0 }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<template>
  <div class="statistics-panel">
    <h2>Platform Overview</h2>
    
    <div class="stats-grid">
      <!-- Users Statistics -->
      <div class="stat-card">
        <div class="stat-title">Users</div>
        <div class="stat-numbers">
          <div>Total: {{ formatNumber(stats?.total_users || 0) }}</div>
          <div>Active: {{ formatNumber(stats?.active_users || 0) }}</div>
        </div>
      </div>

      <!-- Role Statistics -->
      <div class="stat-card">
        <div class="stat-title">User Types</div>
        <div class="stat-numbers">
          <div>Sponsors: {{ formatNumber(stats?.total_sponsors || 0) }}</div>
          <div>Influencers: {{ formatNumber(stats?.total_influencers || 0) }}</div>
        </div>
      </div>

      <!-- Campaign Statistics -->
      <div class="stat-card">
        <div class="stat-title">Campaigns</div>
        <div class="stat-numbers">
          <div>Total: {{ formatNumber(stats?.total_campaigns || 0) }}</div>
          <div>Active: {{ formatNumber(stats?.active_campaigns || 0) }}</div>
        </div>
      </div>

      <!-- Ad Request Statistics -->
      <div class="stat-card">
        <div class="stat-title">Ad Requests</div>
        <div class="stat-numbers">
          <div>Total: {{ formatNumber(stats?.total_ad_requests || 0) }}</div>
          <div>Pending: {{ formatNumber(stats?.pending_ad_requests || 0) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatisticsPanel',
  props: {
    stats: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatNumber(num) {
      return new Intl.NumberFormat().format(num)
    }
  }
}
</script>

<style scoped>
.statistics-panel {
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
  margin: 0 0 1.5rem 0;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.25rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

.stat-title {
  color: #94a3b8;
  font-size: 0.95rem;
  font-weight: 500;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.025em;
}

.stat-numbers {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.stat-numbers div {
  color: #e2e8f0;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-numbers div::before {
  content: '';
  display: inline-block;
  width: 6px;
  height: 6px;
  background: #6366f1;
  border-radius: 50%;
}

/* Different colors for different stat types */
.stat-card:nth-child(1) .stat-numbers div::before {
  background: #6366f1; /* Indigo for Users */
}

.stat-card:nth-child(2) .stat-numbers div::before {
  background: #10b981; /* Emerald for User Types */
}

.stat-card:nth-child(3) .stat-numbers div::before {
  background: #8b5cf6; /* Purple for Campaigns */
}

.stat-card:nth-child(4) .stat-numbers div::before {
  background: #f59e0b; /* Amber for Ad Requests */
}

@media (max-width: 768px) {
  .statistics-panel {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-numbers div {
    font-size: 1.1rem;
  }
}
</style>