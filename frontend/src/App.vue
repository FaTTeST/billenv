<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app" class="min-h-screen bg-stone-50">
    <header class="bg-white shadow-sm border-b border-stone-200">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <router-link to="/" class="text-2xl font-serif text-stone-800">
              PostSocial
            </router-link>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/login" class="text-stone-600 hover:text-stone-900">
              Войти
            </router-link>
            <router-link to="/signup" class="bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700">
              Регистрация
            </router-link>
          </div>
        </div>
      </nav>
    </header>

    <main class="py-8">
      <RouterView />
    </main>

    <footer class="bg-stone-800 text-stone-300 py-8 mt-16">
      <div class="max-w-7xl mx-auto px-4 text-center">
        <p class="font-serif">PostSocial — Ваша лента продолжает жить</p>
        <p class="text-sm mt-2">Там, где интернет заканчивается</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
}
</style>
