<template>
    <div class="callback-page">
      <h2>處理登入中...</h2>
      <p>請稍候，正在完成登入程序</p>
    </div>
  </template>
  
  <script>
  import { defineComponent, onMounted } from 'vue'
  
  export default defineComponent({
    name: 'GoogleCallback',
    setup() {
      onMounted(() => {
        // 這個頁面僅作為 Google OAuth 回調，實際處理在 LoginView 中完成
        // 不需要特別處理，因為使用的是客戶端流程
        window.close()
      })
    }
  })
  </script>
  
  <style scoped>
  .callback-page {
    text-align: center;
    padding: 3rem;
  }
  </style>