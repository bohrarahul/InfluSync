<template>
  <div class="user-management">
    <h2>User Management</h2>

    <!-- Filters -->
    <div class="filters">
      <select v-model="roleFilter" class="filter-select">
        <option value="">All Roles</option>
        <option value="sponsor">Sponsors</option>
        <option value="influencer">Influencers</option>
      </select>
      
      <select v-model="statusFilter" class="filter-select">
        <option value="">All Status</option>
        <option value="true">Active</option>
        <option value="false">Inactive</option>
      </select>
    </div>

    <!-- Loading and Error States -->
    <div v-if="loading" class="loading">Loading users...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <!-- Users Table -->
    <div class="users-table-container" v-if="!loading && filteredUsers.length">
      <table class="users-table">
        <thead>
          <tr>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td class="capitalize">{{ user.role }}</td>
            <td>
              <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td>
              <button 
                @click="toggleUserStatus(user)"
                :disabled="processingId === user.id"
                :class="['toggle-btn', user.is_active ? 'deactivate' : 'activate']"
              >
                {{ processingId === user.id ? 'Processing...' : 
                   user.is_active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No Users Message -->
    <div v-if="!loading && !filteredUsers.length" class="no-data">
      <p>No users found matching the selected filters</p>
      <p class="suggestion">Try adjusting your role or status filters to see more users.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserManagementPanel',
  data() {
    return {
      users: [],
      loading: true,
      error: null,
      processingId: null,
      roleFilter: '',
      statusFilter: ''
    }
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const roleMatch = !this.roleFilter || user.role === this.roleFilter
        const statusMatch = !this.statusFilter || 
          user.is_active === (this.statusFilter === 'true')
        return roleMatch && statusMatch
      })
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      try {
        this.loading = true
        const response = await axios.get('/admin/users')
        this.users = response.data
        this.error = null
      } catch (err) {
        console.error('Error fetching users:', err)
        this.error = 'Failed to load users'
      } finally {
        this.loading = false
      }
    },
    async toggleUserStatus(user) {
      try {
        this.processingId = user.id
        await axios.put(`/admin/users/${user.id}`, {
          is_active: !user.is_active
        })
        
        // Update local state
        const updatedUser = this.users.find(u => u.id === user.id)
        if (updatedUser) {
          updatedUser.is_active = !user.is_active
        }
        
        this.error = null
      } catch (err) {
        console.error('Error toggling user status:', err)
        this.error = 'Failed to update user status'
      } finally {
        this.processingId = null
      }
    }
  }
}
</script>

<style scoped>
.user-management {
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
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.filter-select {
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e2e8f0;
  font-size: 0.95rem;
  min-width: 150px;
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

.users-table-container {
  overflow-x: auto;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.users-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 0;
}

.users-table th,
.users-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: #94a3b8;
}

.users-table th {
  background: rgba(255, 255, 255, 0.03);
  font-weight: 500;
  color: white;
  position: sticky;
  top: 0;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.users-table tr:hover td {
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
  .user-management {
    padding: 1rem;
  }

  .filters {
    flex-direction: column;
  }

  .filter-select {
    width: 100%;
    min-width: 0;
  }

  .users-table td, 
  .users-table th {
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