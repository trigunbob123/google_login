<template>
    <div class="home">
      <h1>歡迎使用 Google 登入系統</h1>
      
      <div class="content">
        <div v-if="isAuthenticated" class="welcome-message">
          <h2>你好，{{ username }}！</h2>
          <p>你已成功登入系統。</p>
          <router-link to="/profile" class="profile-link">查看個人檔案</router-link>
        </div>
        
        <div v-else class="login-prompt">
          <p>你尚未登入。請使用 Google 帳號登入以存取完整功能。</p>
          <router-link to="/login" class="login-link">前往登入</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent, computed } from 'vue'
  import { useStore } from 'vuex'
  
  export default defineComponent({
    name: 'HomeView',
    setup() {
      const store = useStore()
      
      const isAuthenticated = computed(() => store.getters.isAuthenticated)
      const username = computed(() => store.state.user?.username || '')
      
      return {
        isAuthenticated,
        username
      }
    }
  })
  </script>
  
  <style scoped>
  .home {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .content {
    margin-top: 2rem;
    padding: 1.5rem;
    background-color: #f5f5f5;
    border-radius: 8px;
  }
  
  .welcome-message, .login-prompt {
    text-align: center;
  }
  
  .profile-link, .login-link {
    display: inline-block;
    margin-top: 1rem;
    padding: 0.6rem 1.2rem;
    background-color: #1976d2;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: bold;
  }
  
  .profile-link:hover, .login-link:hover {
    background-color: #1565c0;
  }
  </style>