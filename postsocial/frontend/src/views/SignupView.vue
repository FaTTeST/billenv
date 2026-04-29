<template>
  <div class="min-h-screen bg-primary-50 flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full">
      <div class="bg-white rounded-xl shadow-lg p-8">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-primary-700">📮 PostSocial</h1>
          <p class="text-gray-600 mt-2">Регистрация нового аккаунта</p>
        </div>

        <form @submit.prevent="handleRegister" class="space-y-6">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label for="full_name" class="block text-sm font-medium text-gray-700">Имя</label>
            <input
              id="full_name"
              v-model="form.full_name"
              type="text"
              class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
              placeholder="Иван Иванов"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Пароль</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              minlength="8"
              class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-primary-500 focus:border-primary-500"
              placeholder="••••••••"
            />
          </div>

          <div v-if="error" class="text-red-600 text-sm text-center">{{ error }}</div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50"
          >
            {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-gray-600">
            Уже есть аккаунт?
            <router-link to="/login" class="text-primary-600 hover:text-primary-700 font-semibold">
              Войти
            </router-link>
          </p>
        </div>

        <div class="mt-4 text-center">
          <router-link to="/" class="text-gray-500 hover:text-gray-700 text-sm">
            ← На главную
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  full_name: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''
  
  try {
    await authStore.register(form)
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка регистрации. Попробуйте другой email.'
  } finally {
    loading.value = false
  }
}
</script>
