<template>
  <div class="sponsor-layout">
    <!-- Sidebar Navigation -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>Sponsor Dashboard</h2>
      </div>
      
      <nav class="nav-menu">
        <router-link 
          to="/sponsor/dashboard" 
          class="nav-item"
          active-class="active"
        >
          Dashboard
        </router-link>

        <router-link 
          to="/sponsor/campaigns" 
          class="nav-item"
          active-class="active"
        >
          My Campaigns
        </router-link>

        <router-link 
          to="/sponsor/campaigns/new" 
          class="nav-item"
          active-class="active"
        >
          Create Campaign
        </router-link>

        <router-link 
          to="/sponsor/influencers" 
          class="nav-item"
          active-class="active"
        >
          Find Influencers
        </router-link>

        <router-link 
          to="/sponsor/requests" 
          class="nav-item"
          active-class="active"
        >
          Ad Requests
        </router-link>
      </nav>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SponsorLayout'
}
</script>

<style scoped>
.sponsor-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 20px 0;
  position: fixed;
  height: 100vh;
  left: 0;
  top: 0;
}

.sidebar-header {
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: white;
}

.nav-menu {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
}

.nav-item {
  padding: 12px 20px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.nav-item.active {
  background: rgba(255,255,255,0.1);
  color: white;
  border-left-color: #3498db;
}

.main-content {
  flex: 1;
  margin-left: 250px;
  padding: 20px;
  background: #f5f6fa;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }
  
  .main-content {
    margin-left: 200px;
  }
}

@media (max-width: 576px) {
  .sponsor-layout {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  
  .main-content {
    margin-left: 0;
  }
  
  .nav-menu {
    flex-direction: row;
    overflow-x: auto;
    padding: 10px;
  }
  
  .nav-item {
    padding: 8px 15px;
    border-left: none;
    border-bottom: 3px solid transparent;
  }
  
  .nav-item.active {
    border-left-color: transparent;
    border-bottom-color: #3498db;
  }
}
</style>