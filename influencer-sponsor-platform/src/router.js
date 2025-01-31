import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './views/auth/Login.vue'
import Register from './views/auth/Register.vue'
import AdminDashboard from './views/admin/Dashboard.vue'
import SponsorDashboard from './views/sponsor/Dashboard.vue'
import InfluencerDashboard from './views/influencer/Dashboard.vue'
import CampaignManagement from './views/sponsor/CampaignManagement.vue'
import CreateCampaign from './views/sponsor/CreateCampaign.vue'
import InfluencerSearch from '@/views/sponsor/InfluencerSearch.vue'
import AdRequestManagement from '@/views/sponsor/AdRequestManagement.vue' 
import BrowseCampaigns from '@/views/influencer/BrowseCampaigns.vue'
import CampaignDetails from '@/views/influencer/CampaignDetails.vue'
import InfluencerRequestManagement from '@/views/influencer/InfluencerRequestManagement.vue'
import ProfileManagement from '@/views/influencer/ProfileManagement.vue'
import CampaignExport from '@/views/sponsor/CampaignExport.vue'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true, role: 'admin' }
    },
    {
      path: '/influencer/dashboard',
      name: 'influencer-dashboard',
      component: InfluencerDashboard,
      meta: { requiresAuth: true, role: 'influencer' }
    },
    {
      path: '/sponsor/dashboard',
      name: 'sponsor-dashboard',
      component: SponsorDashboard,
      meta: { requiresAuth: true, role: 'sponsor' }
    },

    {
      path: '/sponsor/campaigns',
      name: 'sponsor-campaigns',
      component: CampaignManagement,
      meta: { requiresAuth: true, role: 'sponsor' }
    },
    {
      path: '/sponsor/campaigns/new',
      name: 'create-campaign',
      component: CreateCampaign,
      meta: { requiresAuth: true, role: 'sponsor' }
    },
    {
      path: '/sponsor/influencers',
      name: 'influencer-search',
      component: InfluencerSearch,
      meta: { requiresAuth: true, role: 'sponsor' }
    },
    {
      path: '/sponsor/requests',
      name: 'ad-requests',
      component: AdRequestManagement,
      meta: { requiresAuth: true, role: 'sponsor' }
    },
    {
      path: '/influencer/campaigns',
      name: 'browse-campaigns',
      component: BrowseCampaigns,
      meta: { requiresAuth: true, role: 'influencer' }
    },
    {
      path: '/influencer/campaigns/:id',
      name: 'campaign-details',
      component: CampaignDetails,
      meta: { requiresAuth: true, role: 'influencer' }
    },
    {
      path: '/influencer/requests',
      name: 'influencer-requests',
      component: InfluencerRequestManagement,
      meta: { requiresAuth: true, role: 'influencer' }
    },
    {
      path: '/influencer/profile',
      name: 'influencer-profile',
      component: ProfileManagement,
      meta: { requiresAuth: true, role: 'influencer' }
    },
    {
      path: '/sponsor/export',
      name: 'campaign-export',
      component: CampaignExport,
      meta: { requiresAuth: true, role: 'sponsor' }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('userRole')

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!token) {
      next('/login')
    } else if (to.meta.role && to.meta.role !== role) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router