<template>
    <div class="profile-page">
      <h1>個人資料</h1>
      
      <div v-if="isLoading">載入中...</div>
      
      <div v-else-if="user" class="profile-container">
        <div class="profile-header">
          <img v-if="user.profile_image" :src="user.profile_image" class="profile-image" alt="Profile" />
          <h2>{{ user.username }}</h2>
        </div>
        
        <div class="profile-details">
          <p><strong>Email:</strong> {{ user.email }}</p>
        </div>
      </div>
      
      <button @click="handleLogout" class="logout-btn">登出</button>
    </div>
  </template>
  
  <script>
  import { defineComponent, computed } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  
  export default defineComponent({
    name: 'ProfileView',
    setup() {
      const store = useStore()
      const router = useRouter()
      
      const user = computed(() => store.state.user)
      const isLoading = computed(() => store.state.loading)
      
      const handleLogout = async () => {
        await store.dispatch('logout')
        router.push('/login')
      }
      
      return {
        user,
        isLoading,
        handleLogout
      }
    }
  })
  </script>
  
  <style scoped>
  .profile-page {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .profile-container {
    margin-top: 2rem;
  }
  
  .profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;
  }
  
  .profile-image {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin-right: 1rem;
  }
  
  .profile-details {
    background-color: #f5f5f5;
    padding: 1rem;
    border-radius: 8px;
  }
  
  .logout-btn {
    margin-top: 2rem;
    background-color: #f44336;
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    cursor: pointer;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .logout-btn:hover {
    background-color: #d32f2f;
  }
  </style>