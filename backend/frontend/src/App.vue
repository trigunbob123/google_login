<template>
  <div class="app">
    <header>
      <nav>
        <router-link to="/">首頁</router-link>
        <template v-if="isAuthenticated">
          <router-link to="/profile">個人資料</router-link>
        </template>
        <template v-else>
          <router-link to="/login">登入</router-link>
        </template>
      </nav>
    </header>
    
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import { defineComponent, computed, onMounted } from 'vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'App',
  setup() {
    const store = useStore()
    
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    
    onMounted(async () => {
      if (localStorage.getItem('accessToken')) {
        try {
          await store.dispatch('fetchCurrentUser')
        } catch (error) {
          console.error('自動登入失敗：', error)
        }
      }
    })
    
    return {
      isAuthenticated
    }
  }
})
</script>

<style>
.app {
  font-family: 'Microsoft JhengHei', Arial, sans-serif;
}

header {
  background-color: #f8f9fa;
  padding: 1rem;
  margin-bottom: 2rem;
}

nav {
  display: flex;
  gap: 1.5rem;
}

nav a {
  color: #333;
  text-decoration: none;
}

nav a.router-link-active {
  font-weight: bold;
  color: #1976d2;
}

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}
</style>