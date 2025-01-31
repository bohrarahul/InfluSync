<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-bg">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        <div class="circle circle-3"></div>
      </div>

      <div class="hero-content">
        <div class="animated-title">
          <div class="line">Transform Your</div>
          <div class="gradient-line">Digital Presence</div>
        </div>
        
        <p class="hero-subtitle">Connect with the perfect partners for your brand journey</p>
        
        <div class="cta-buttons">
          <router-link to="/register" class="cta-button primary">
            Get Started
            <span class="shine"></span>
          </router-link>
          <router-link to="/login" class="cta-button secondary">
            <span>Explore Platform</span>
          </router-link>
        </div>

        <div class="achievement-cards">
          <div class="achievement-card">
            <div class="achievement-icon">⭐</div>
            <div class="achievement-number">500+</div>
            <div class="achievement-text">Active Brands</div>
          </div>
          <div class="achievement-card premium">
            <div class="achievement-icon">🚀</div>
            <div class="achievement-number">15K+</div>
            <div class="achievement-text">Collaborations</div>
          </div>
          <div class="achievement-card">
            <div class="achievement-icon">👥</div>
            <div class="achievement-number">2.5K</div>
            <div class="achievement-text">Creators</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features">
      <h2 class="section-title">Choose Your Journey</h2>
      
      <div class="feature-container">
        <!-- Brand Card -->
        <div class="feature-card">
          <div class="card-content">
            <div class="feature-icon brand">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 7H4C2.89543 7 2 7.89543 2 9V19C2 20.1046 2.89543 21 4 21H20C21.1046 21 22 20.1046 22 19V9C22 7.89543 21.1046 7 20 7Z"/>
              </svg>
            </div>
            <h3>For Brands</h3>
            <p>Launch impactful campaigns with creators who truly understand your vision</p>
            <ul class="feature-list">
              <li>Smart creator matching</li>
              <li>Campaign analytics</li>
              <li>Brand performance insights</li>
            </ul>
            <div class="card-action">
              <router-link to="/register?type=brand" class="action-link">
                Start Your Campaign
                <span class="arrow">→</span>
              </router-link>
            </div>
          </div>
        </div>

        <!-- Creator Card -->
        <div class="feature-card">
          <div class="card-content">
            <div class="feature-icon creator">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 15C15.866 15 19 11.866 19 8C19 4.134 15.866 1 12 1C8.13401 1 5 4.134 5 8C5 11.866 8.13401 15 12 15Z"/>
              </svg>
            </div>
            <h3>For Creators</h3>
            <p>Turn your influence into lasting partnerships with leading brands</p>
            <ul class="feature-list">
              <li>Brand collaboration tools</li>
              <li>Growth analytics</li>
              <li>Performance tracking</li>
            </ul>
            <div class="card-action">
              <router-link to="/register?type=creator" class="action-link">
                Join as Creator
                <span class="arrow">→</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>

<style scoped>
.home {
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  min-height: calc(100vh - 64px);
  color: white;
  overflow: hidden;
}

/* Hero Section */
.hero {
  position: relative;
  padding: 80px 20px;
  overflow: hidden;
}

.hero-bg {
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

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.animated-title {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 24px;
}

.animated-title .line {
  color: white;
}

.gradient-line {
  background: linear-gradient(135deg, #60a5fa 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: 20px;
  color: #94a3b8;
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* CTA Buttons */
.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-bottom: 60px;
}

.cta-button {
  position: relative;
  padding: 14px 32px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 16px;
  text-decoration: none;
  transition: all 0.3s ease;
  overflow: hidden;
}

.cta-button.primary {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white;
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shine 3s infinite;
}

@keyframes shine {
  100% {
    left: 100%;
  }
}

/* Achievement Cards */
.achievement-cards {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-wrap: wrap;
}

.achievement-card {
  background: rgba(255, 255, 255, 0.05);
  padding: 24px;
  border-radius: 16px;
  min-width: 180px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease;
}

.achievement-card:hover {
  transform: translateY(-5px);
  border-color: rgba(99, 102, 241, 0.5);
}

.achievement-card.premium {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.1) 100%);
  border-color: rgba(99, 102, 241, 0.2);
}

.achievement-icon {
  font-size: 24px;
  margin-bottom: 12px;
}

.achievement-number {
  font-size: 36px;
  font-weight: 700;
  color: #6366f1;
  margin-bottom: 8px;
}

.achievement-text {
  color: #94a3b8;
}

/* Features Section */
.features {
  padding: 80px 20px;
  background: rgba(255, 255, 255, 0.02);
}

.section-title {
  text-align: center;
  font-size: 40px;
  font-weight: 700;
  margin-bottom: 60px;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.feature-container {
  display: flex;
  gap: 30px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.feature-card {
  flex: 1;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  padding: 40px;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  border-color: rgba(99, 102, 241, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.feature-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.feature-icon.brand {
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
}

.feature-icon.creator {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
}

.feature-icon svg {
  width: 30px;
  height: 30px;
  color: white;
}

.feature-card h3 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 16px;
}

.feature-card p {
  color: #94a3b8;
  margin-bottom: 24px;
  line-height: 1.6;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
}

.feature-list li {
  color: #94a3b8;
  margin-bottom: 12px;
  padding-left: 24px;
  position: relative;
}

.feature-list li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: #6366f1;
}

.action-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-link:hover {
  color: #818cf8;
  gap: 12px;
}

.arrow {
  transition: transform 0.3s ease;
}

.action-link:hover .arrow {
  transform: translateX(5px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .animated-title {
    font-size: 40px;
  }

  .feature-container {
    flex-direction: column;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
    padding: 0 20px;
  }

  .achievement-cards {
    flex-direction: column;
    align-items: center;
  }

  .achievement-card {
    width: 100%;
    max-width: 300px;
  }
}
</style>