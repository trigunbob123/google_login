import { createStore } from 'vuex'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

// 設置 axios 攔截器，自動添加 token 到請求頭
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default createStore({
  state: {
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },
    SET_LOADING(state, status) {
      state.loading = status
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    LOGOUT(state) {
      state.user = null
      state.isAuthenticated = false
    }
  },
  actions: {
    // Google 登入
    async googleLogin({ commit }, { idToken }) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      console.log('xxxxxx');
      
      
      try {
        const response = await axios.post(`${API_URL}/auth/google/`, {
            id_token: idToken 
        })
        
        // 存儲 token
        localStorage.setItem('idToken', response.data.access)
        localStorage.setItem('refreshToken', response.data.refresh)
        
        // 設置使用者
        commit('SET_USER', response.data.user)
        
        return response.data.user
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.error || '登入失敗')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 獲取當前使用者資訊
    async fetchCurrentUser({ commit }) {
      if (!localStorage.getItem('accessToken')) {
        return null
      }
      
      commit('SET_LOADING', true)
      
      try {
        const response = await axios.get(`${API_URL}/user/me/`)
        commit('SET_USER', response.data)
        return response.data
      } catch (error) {
        commit('SET_ERROR', '獲取用戶資訊失敗')
        commit('LOGOUT')
        // 清除 token
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        throw error
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    // 登出
    logout({ commit }) {
      commit('LOGOUT')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    }
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    isLoading: state => state.loading,
    error: state => state.error
  }
})