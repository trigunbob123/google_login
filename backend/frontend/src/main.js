import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vue3GoogleLogin from 'vue3-google-login'

const app = createApp(App)

app.use(router)
app.use(store)
app.use(vue3GoogleLogin, {
  clientId: 'YOUR_CLIENT_ID',  // 請填入自己的 Google API 專案 Client ID
  prompt: 'select_account',  // 添加此選項，確保每次都顯示帳號選擇界面
  scope: 'email profile',     // 指定所需權限
  ux_mode: 'popup'           // 使用彈出式視窗模式，避免跨域問題
})

app.mount('#app')

