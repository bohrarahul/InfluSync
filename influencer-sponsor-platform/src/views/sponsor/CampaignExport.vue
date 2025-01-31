<template>
  <div class="campaign-export">
    <!-- Background Elements -->
    <div class="dashboard-bg">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="dashboard-content">
      <div class="dashboard-header">
        <h1>Export Campaign Data</h1>
        <p class="header-subtitle">Download and analyze your campaign performance</p>
      </div>

      <div class="dashboard-section export-section">
        <div class="export-info">
          <div class="section-header">
            <h2>Download Campaign Report</h2>
          </div>
          
          <div class="info-card">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <p>Your export will include:</p>
            <ul>
              <li>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 5l7 7-7 7"/>
                </svg>
                Campaign titles and descriptions
              </li>
              <li>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 5l7 7-7 7"/>
                </svg>
                Start and end dates
              </li>
              <li>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 5l7 7-7 7"/>
                </svg>
                Budget information
              </li>
              <li>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 5l7 7-7 7"/>
                </svg>
                Status and categories
              </li>
            </ul>
          </div>
        </div>

        <!-- Export Actions -->
        <div class="action-section">
          <button 
            @click="startExport"
            :disabled="exporting"
            class="action-btn export-btn"
          >
            <svg v-if="!exporting" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
            </svg>
            <svg v-else class="spinner" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
            </svg>
            {{ exporting ? 'Generating Export...' : 'Generate Export' }}
          </button>
          
          <div v-if="exportStatus" 
               :class="['status-message', { 'error': exportStatus.includes('Failed') }]">
            <svg v-if="exportStatus.includes('Failed')" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            {{ exportStatus }}
          </div>
        </div>

        <!-- Recent Exports -->
        <div v-if="recentFile" class="dashboard-section recent-export">
          <div class="section-header">
            <h3>Recent Export</h3>
          </div>
          <div class="file-info">
            <div class="file-details">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              <span>{{ recentFile }}</span>
            </div>
            <button 
              @click="downloadFile(recentFile)"
              class="action-btn download-btn"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>
              </svg>
              Download
            </button>
          </div>
        </div>
      </div>

      <!-- Notification Info -->
      <div class="dashboard-section notification-info">
        <div class="info-content">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <p>You will receive an email notification when your export is ready.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'CampaignExport',
  data() {
    return {
      exporting: false,
      exportStatus: '',
      recentFile: null
    }
  },
  methods: {
    async startExport() {
      try {
        this.exporting = true
        this.exportStatus = 'Starting export process...'
        
        const response = await axios.get('/export_campaigns')
        this.exportStatus = response.data.message
        
        // Reset status after 5 seconds
        setTimeout(() => {
          this.exportStatus = ''
        }, 5000)
      } catch (err) {
        console.error('Export error:', err)
        this.exportStatus = 'Failed to start export. Please try again.'
      } finally {
        this.exporting = false
      }
    },
    async downloadFile(filename) {
      try {
        const response = await axios.get(`/download_export/${filename}`, {
          responseType: 'blob'
        })
        
        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (err) {
        console.error('Download error:', err)
        alert('Failed to download file. Please try again.')
      }
    }
  }
}

</script>
<style scoped>
.campaign-export {
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
  max-width: 800px;
  margin: 0 auto;
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

.dashboard-section {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease;
  margin-bottom: 1.5rem;
}

.dashboard-section:hover {
  transform: translateY(-5px);
}

.section-header {
  margin-bottom: 1.5rem;
}

.section-header h2, 
.section-header h3 {
  color: #fff;
  font-size: 1.5rem;
  margin: 0;
}

/* Info Card */
.info-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.5rem;
  margin: 1rem 0;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.card-icon {
  width: 48px;
  height: 48px;
  color: #6366f1;
  margin-bottom: 1rem;
}

.info-card p {
  color: #94a3b8;
  margin-bottom: 1rem;
}

.info-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-card li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #fff;
  margin-bottom: 0.75rem;
}

.info-card li svg {
  width: 16px;
  height: 16px;
  color: #6366f1;
}

/* Action Section */
.action-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 0;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn svg {
  width: 20px;
  height: 20px;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.action-btn.export-btn {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
}

.action-btn.export-btn:hover {
  background: rgba(34, 197, 94, 0.2);
}

.action-btn.download-btn {
  background: rgba(59, 130, 246, 0.1);
  color: #60a5fa;
}

.action-btn.download-btn:hover {
  background: rgba(59, 130, 246, 0.2);
}

/* Status Message */
.status-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
}

.status-message.error {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}

.status-message svg {
  width: 20px;
  height: 20px;
}

/* Recent Export */
.file-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.file-details {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #fff;
}

.file-details svg {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

/* Notification Info */
.notification-info .info-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: #94a3b8;
}

.notification-info svg {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

/* Spinner Animation */
.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-content {
    padding: 1rem;
  }

  .dashboard-header h1 {
    font-size: 2rem;
  }

  .dashboard-section {
    padding: 1.25rem;
  }

  .info-card {
    padding: 1.25rem;
  }

  .file-info {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.75rem;
  }

  .header-subtitle {
    font-size: 1rem;
  }

  .section-header h2,
  .section-header h3 {
    font-size: 1.25rem;
  }

  .info-card {
    padding: 1rem;
  }

  .card-icon {
    width: 36px;
    height: 36px;
  }

  .status-message {
    text-align: center;
    flex-direction: column;
  }
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Hover Effects */
.dashboard-section {
  transition: all 0.3s ease;
}

.dashboard-section:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.info-card:hover {
  transform: translateY(-2px);
  border-color: rgba(255, 255, 255, 0.2);
}

/* Enhanced Focus States */
.action-btn:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.4);
}

.action-btn:focus:not(:focus-visible) {
  box-shadow: none;
}

/* Loading State */
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.loading .spinner {
  width: 40px;
  height: 40px;
  color: #6366f1;
}

/* Progress States */
.progress-indicator {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin: 1rem 0;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #818cf8);
  transition: width 0.3s ease;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 2rem;
  color: #94a3b8;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #6366f1;
  opacity: 0.5;
  margin-bottom: 1rem;
}

/* Error State */
.error-state {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  padding: 1rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #f87171;
  margin: 1rem 0;
}

.error-state svg {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}
</style>