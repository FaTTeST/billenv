<template>
  <div class="min-h-screen bg-primary-50">
    <!-- Dashboard Header -->
    <header class="bg-white shadow-sm">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-primary-700">📮 PostSocial</h1>
          <div class="flex items-center space-x-4">
            <span v-if="authStore.user" class="text-gray-600">{{ authStore.user.full_name || authStore.user.email }}</span>
            <button @click="logout" class="text-primary-600 hover:text-primary-700">Выйти</button>
          </div>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-8">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-primary-800">Личный кабинет</h2>
        <p class="text-gray-600 mt-2">Управляйте подпиской и получателями</p>
      </div>

      <!-- Quick Stats -->
      <div class="grid md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow p-6">
          <h3 class="text-lg font-semibold text-gray-700">Активная подписка</h3>
          <p class="text-3xl font-bold text-primary-600 mt-2">—</p>
          <p class="text-sm text-gray-500 mt-1">Нет активной подписки</p>
        </div>
        <div class="bg-white rounded-xl shadow p-6">
          <h3 class="text-lg font-semibold text-gray-700">Получатели</h3>
          <p class="text-3xl font-bold text-primary-600 mt-2">0</p>
          <p class="text-sm text-gray-500 mt-1">Добавьте первого получателя</p>
        </div>
        <div class="bg-white rounded-xl shadow p-6">
          <h3 class="text-lg font-semibold text-gray-700">Отправлено писем</h3>
          <p class="text-3xl font-bold text-primary-600 mt-2">0</p>
          <p class="text-sm text-gray-500 mt-1">История отправок</p>
        </div>
      </div>

      <!-- Action Cards -->
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <router-link to="/sources" class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition">
          <div class="text-4xl mb-4">🔗</div>
          <h3 class="text-lg font-semibold text-gray-700">Источники контента</h3>
          <p class="text-gray-500 text-sm mt-2">Подключите Instagram, VK или Telegram</p>
        </router-link>

        <router-link to="/recipients" class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition">
          <div class="text-4xl mb-4">👥</div>
          <h3 class="text-lg font-semibold text-gray-700">Получатели</h3>
          <p class="text-gray-500 text-sm mt-2">Добавьте адреса близких</p>
        </router-link>

        <router-link to="/subscription" class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition">
          <div class="text-4xl mb-4">💳</div>
          <h3 class="text-lg font-semibold text-gray-700">Подписка</h3>
          <p class="text-gray-500 text-sm mt-2">Выберите тарифный план</p>
        </router-link>

        <router-link to="/settings" class="bg-white rounded-xl shadow p-6 hover:shadow-lg transition">
          <div class="text-4xl mb-4">⚙️</div>
          <h3 class="text-lg font-semibold text-gray-700">Настройки</h3>
          <p class="text-gray-500 text-sm mt-2">Профиль и уведомления</p>
        </router-link>
      </div>
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function logout() {
  authStore.logout()
  router.push('/')
}
</script>
