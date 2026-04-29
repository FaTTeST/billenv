# PostSocial Frontend

Клиентское веб-приложение на Vue 3 + Vite.

## Структура проекта

```
frontend/
├── src/
│   ├── api/          # API клиенты
│   ├── assets/       # Статические файлы
│   ├── components/   # Vue компоненты
│   ├── composables/  # Composition API функции
│   ├── router/       # Vue Router конфигурация
│   ├── stores/       # Pinia store'ы
│   └── views/        # Страницы приложения
├── public/           # Публичные файлы
├── index.html
├── package.json
└── vite.config.js
```

## Установка

```bash
npm install
```

## Запуск разработки

```bash
npm run dev
```

## Сборка для продакшена

```bash
npm run build
```

## Технологический стек

- Vue 3 (Composition API)
- Vue Router
- Pinia (state management)
- Vite (сборка)
- Tailwind CSS + Headless UI
- Axios (HTTP клиент)
