<template>
    <div class="login-page">
      <h1>使用者登入</h1>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <div class="google-login-container">
        <GoogleLogin :callback="handleGoogleLogin" />
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent, computed } from 'vue'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  import { GoogleLogin } from 'vue3-google-login'
  
  export default defineComponent({
    name: 'LoginView',
    setup() {
      const store = useStore()
      const router = useRouter()
      
      const error = computed(() => store.state.error)
      
      const handleGoogleLogin = async (response) => {
       try {
          console.log('Google 登入回應:', response);
          
          // Google 會返回 credential 而不是 access_token
          if (response.credential) {
            console.log(response.credential);
            
            // 使用 ID token 而不是 access token
            await store.dispatch('googleLogin', {
              idToken: response.credential
            });
          } else {
            console.error('Google 登入未返回有效憑證');
          }
          router.push('/')
        } catch (err) {
          console.error('Google 登入失敗:', err)
        }
      }
      
      return {
        error,
        handleGoogleLogin
      }
    }
  })
  </script>
  
  <style scoped>
  .login-page {
    max-width: 500px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  .google-login-container {
    margin-top: 2rem;
    display: flex;
    justify-content: center;
  }
  
  .error-message {
    color: red;
    margin-bottom: 1rem;
    padding: 0.5rem;
    background-color: #ffecec;
    border-radius: 4px;
  }
  </style>