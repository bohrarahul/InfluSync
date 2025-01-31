<template>
  <div id="app">
    <nav v-if="!isAuthRoute" class="navbar" :class="{ 'navbar-scrolled': scrolled }">
      <div class="nav-container">
        <router-link to="/" class="nav-brand">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7L12 12L22 7L12 2Z"/>
              <path d="M2 17L12 22L22 17"/>
              <path d="M2 12L12 17L22 12"/>
            </svg>
          </div>
          <span class="brand-text">Influencer Connect</span>
        </router-link>

        <div class="nav-menu">
          <template v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link">
              <span>Login</span>
            </router-link>
            <router-link to="/register" class="nav-button">
              <span>Register</span>
              <span class="shine"></span>
            </router-link>
          </template>
          <template v-else>
            <div class="user-menu" @click="toggleDropdown" ref="userMenu">
              <div class="user-avatar">
                {{ username.charAt(0).toUpperCase() }}
              </div>
              <span class="username">{{ username }}</span>
              <svg class="dropdown-arrow" :class="{ 'rotated': dropdownOpen }" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9L12 15L18 9"/>
              </svg>

              <!-- Dropdown Menu -->
              <div v-if="dropdownOpen" class="dropdown-menu">
                <router-link to="/profile" class="dropdown-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21"/>
                    <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"/>
                  </svg>
                  <span>Profile</span>
                </router-link>
                <div class="dropdown-divider"></div>
                <a href="#" @click.prevent="logout" class="dropdown-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9"/>
                    <path d="M16 17L21 12L16 7"/>
                    <path d="M21 12H9"/>
                  </svg>
                  <span>Logout</span>
                </a>
              </div>
            </div>
          </template>
        </div>
      </div>
    </nav>

    <main :class="{ 'with-nav': !isAuthRoute }">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      username: localStorage.getItem('username') || '',
      scrolled: false,
      dropdownOpen: false
    }
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
    isAuthRoute() {
      return ['login', 'register'].includes(this.$route.name)
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      localStorage.removeItem('userRole')
      this.dropdownOpen = false
      this.$router.push('/login')
    },
    handleScroll() {
      this.scrolled = window.scrollY > 20
    },
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen
    },
    handleClickOutside(event) {
      if (this.$refs.userMenu && !this.$refs.userMenu.contains(event.target)) {
        this.dropdownOpen = false
      }
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll)
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll)
    document.removeEventListener('click', this.handleClickOutside)
  }
}
</script>

<style>
/* Reset default styles */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0;
  background: #0f172a;
  min-height: 100vh;
}

#app {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background: #0f172a;
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 70px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
  z-index: 1000;
}

.navbar-scrolled {
  background: rgba(15, 23, 42, 0.95);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
}

.brand-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-icon svg {
  width: 24px;
  height: 24px;
  stroke: white;
}

.brand-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #fff 0%, #94a3b8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #94a3b8;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  padding: 8px 16px;
  border-radius: 8px;
}

.nav-link:hover {
  color: white;
  background: rgba(255, 255, 255, 0.1);
}

.nav-button {
  position: relative;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  color: white;
  text-decoration: none;
  padding: 8px 20px;
  border-radius: 8px;
  font-weight: 500;
  overflow: hidden;
  transition: all 0.3s ease;
}

.nav-button:hover {
  transform: translateY(-2px);
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

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.user-menu:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
}

.username {
  color: #94a3b8;
  font-weight: 500;
}

.dropdown-arrow {
  width: 16px;
  height: 16px;
  stroke: #94a3b8;
  transition: transform 0.3s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px;
  min-width: 200px;
  backdrop-filter: blur(10px);
  transform-origin: top right;
  animation: dropdownAppear 0.2s ease;
}

@keyframes dropdownAppear {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  color: #94a3b8;
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.dropdown-item svg {
  width: 16px;
  height: 16px;
  stroke: currentColor;
}

.dropdown-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 8px 0;
}

.with-nav {
  padding-top: 70px;
}

@media (max-width: 640px) {
  .username {
    display: none;
  }
  
  .nav-brand .brand-text {
    display: none;
  }

  .nav-link span {
    display: none;
  }

  .nav-button {
    padding: 8px 16px;
  }
}
</style>