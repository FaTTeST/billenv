import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(credentials) {
    const response = await authApi.login(credentials)
    token.value = response.data.access_token
    localStorage.setItem('access_token', token.value)
    
    // Загружаем информацию о пользователе
    await fetchUser()
    
    return response
  }

  async function register(userData) {
    const response = await authApi.register(userData)
    return response
  }

  async function fetchUser() {
    if (!token.value) return
    
    try {
      const response = await authApi.getMe()
      user.value = response.data
    } catch (error) {
      logout()
      throw error
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    register,
    fetchUser,
    logout,
  }
})
