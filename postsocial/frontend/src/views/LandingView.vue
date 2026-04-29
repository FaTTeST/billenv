<template>
  <div class="min-h-screen bg-primary-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-primary-700">📮 PostSocial</h1>
          </div>
          <div class="flex items-center space-x-4">
            <a href="/login" class="text-primary-600 hover:text-primary-700">Войти</a>
            <a href="/signup" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
              Начать бесплатно
            </a>
          </div>
        </div>
      </nav>
    </header>

    <!-- Hero Section -->
    <section class="py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-5xl font-bold text-primary-800 mb-6">
          Ваша лента продолжает жить —<br />там, где интернет заканчивается
        </h2>
        <p class="text-xl text-gray-600 mb-8">
          Первый в мире сервис-подписка, который автоматически превращает ваши публикации 
          в социальных сетях в реальные бумажные открытки и доставляет их почтой близким людям.
        </p>
        <div class="flex justify-center space-x-4">
          <a href="/signup" class="bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700">
            Попробовать бесплатно
          </a>
          <a href="#how-it-works" class="border-2 border-primary-600 text-primary-600 px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-50">
            Как это работает
          </a>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section id="how-it-works" class="py-20 bg-white">
      <div class="max-w-6xl mx-auto px-4">
        <h3 class="text-3xl font-bold text-center text-primary-800 mb-12">Как это работает</h3>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center p-6">
            <div class="text-5xl mb-4">🔗</div>
            <h4 class="text-xl font-semibold mb-2">1. Подключите соцсети</h4>
            <p class="text-gray-600">
              Свяжите Instagram, VK или Telegram-канал. Сервис будет автоматически забирать новые публикации.
            </p>
          </div>
          <div class="text-center p-6">
            <div class="text-5xl mb-4">👥</div>
            <h4 class="text-xl font-semibold mb-2">2. Добавьте получателей</h4>
            <p class="text-gray-600">
              Укажите адреса бабушек, родителей или друзей. Выберите частоту отправок для каждого.
            </p>
          </div>
          <div class="text-center p-6">
            <div class="text-5xl mb-4">📬</div>
            <h4 class="text-xl font-semibold mb-2">3. Получайте радость</h4>
            <p class="text-gray-600">
              Ваши близкие получают тёплые бумажные письма с вашими фото и историями.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Tariffs -->
    <section class="py-20 bg-primary-50">
      <div class="max-w-6xl mx-auto px-4">
        <h3 class="text-3xl font-bold text-center text-primary-800 mb-12">Тарифы</h3>
        <div class="grid md:grid-cols-3 gap-8">
          <!-- Tarif 1 -->
          <div class="bg-white rounded-xl shadow-lg p-8">
            <h4 class="text-2xl font-bold text-primary-700 mb-2">Привет, бабушке</h4>
            <p class="text-gray-500 mb-4">Для регулярной связи с родными</p>
            <div class="text-4xl font-bold text-primary-800 mb-6">590 ₽<span class="text-lg font-normal">/мес</span></div>
            <ul class="space-y-3 mb-8">
              <li class="flex items-center">✓ 4 открытки в месяц</li>
              <li class="flex items-center">✓ 1 раз в неделю</li>
              <li class="flex items-center">✓ 1 получатель</li>
              <li class="flex items-center">✓ Автопродление</li>
            </ul>
            <a href="/signup" class="block text-center bg-primary-100 text-primary-700 py-3 rounded-lg font-semibold hover:bg-primary-200">
              Выбрать тариф
            </a>
          </div>

          <!-- Tarif 2 -->
          <div class="bg-white rounded-xl shadow-lg p-8 ring-2 ring-primary-500 relative">
            <div class="absolute top-0 right-0 bg-primary-500 text-white px-3 py-1 rounded-bl-lg rounded-tr-lg text-sm">
              Популярный
            </div>
            <h4 class="text-2xl font-bold text-primary-700 mb-2">Цифровой детокс</h4>
            <p class="text-gray-500 mb-4">Для осознанного потребления</p>
            <div class="text-4xl font-bold text-primary-800 mb-6">990 ₽<span class="text-lg font-normal">/мес</span></div>
            <ul class="space-y-3 mb-8">
              <li class="flex items-center">✓ 8 писем в месяц</li>
              <li class="flex items-center">✓ 2 раза в неделю</li>
              <li class="flex items-center">✓ Несколько получателей</li>
              <li class="flex items-center">✓ Приоритетная печать</li>
            </ul>
            <a href="/signup" class="block text-center bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700">
              Выбрать тариф
            </a>
          </div>

          <!-- Tarif 3 -->
          <div class="bg-white rounded-xl shadow-lg p-8">
            <h4 class="text-2xl font-bold text-primary-700 mb-2">Письмо себе</h4>
            <p class="text-gray-500 mb-4">Персональная капсула времени</p>
            <div class="text-4xl font-bold text-primary-800 mb-6">390 ₽<span class="text-lg font-normal">/мес</span></div>
            <ul class="space-y-3 mb-8">
              <li class="flex items-center">✓ 1 письмо в месяц</li>
              <li class="flex items-center">✓ Развёрнутый формат</li>
              <li class="flex items-center">✓ Архив месяца</li>
              <li class="flex items-center">✓ Премиум бумага</li>
            </ul>
            <a href="/signup" class="block text-center bg-primary-100 text-primary-700 py-3 rounded-lg font-semibold hover:bg-primary-200">
              Выбрать тариф
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-primary-800 text-white py-12">
      <div class="max-w-6xl mx-auto px-4">
        <div class="grid md:grid-cols-3 gap-8">
          <div>
            <h5 class="text-xl font-bold mb-4">📮 PostSocial</h5>
            <p class="text-primary-200">
              Возвращаем бумаге статус носителя любви и заботы.
            </p>
          </div>
          <div>
            <h5 class="font-semibold mb-4">Контакты</h5>
            <p class="text-primary-200">support@postsocial.ru</p>
          </div>
          <div>
            <h5 class="font-semibold mb-4">Документы</h5>
            <a href="#" class="block text-primary-200 hover:text-white">Политика конфиденциальности</a>
            <a href="#" class="block text-primary-200 hover:text-white">Оферта</a>
          </div>
        </div>
        <div class="border-t border-primary-700 mt-8 pt-8 text-center text-primary-300">
          © 2024 PostSocial. Все права защищены.
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
// Landing page компонент
</script>
