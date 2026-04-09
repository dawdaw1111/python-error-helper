<template>
  <div class="app-shell">
    <AppHeader />
    <main class="page-shell">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterView } from 'vue-router'

import { ensureAuthInitialized } from './auth'
import AppHeader from './components/AppHeader.vue'

onMounted(async () => {
  await ensureAuthInitialized()
})
</script>
