<template>
  <header class="topbar">
    <RouterLink class="brand" to="/">
      <BrandMark />
      <div>
        <strong>PyErr</strong>
        <span>Python 报错助手</span>
      </div>
    </RouterLink>

    <nav class="topnav">
      <RouterLink class="topnav-link" to="/" exact-active-class="is-active">首页</RouterLink>
      <RouterLink class="topnav-link" to="/search" active-class="is-active">搜索</RouterLink>
    </nav>

    <div class="header-actions">
      <button class="status-pill status-pill-button" type="button" @click="handlePrimaryAction">
        {{ authState.token ? '进入后台' : '登录' }}
      </button>
      <button
        v-if="authState.token"
        class="header-text-button"
        type="button"
        @click="handleLogout"
      >
        退出
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'

import { authState, clearAuth } from '../auth'
import BrandMark from './BrandMark.vue'

const router = useRouter()

function handlePrimaryAction() {
  if (authState.token) {
    router.push({ name: 'admin' })
    return
  }

  router.push({ name: 'login' })
}

function handleLogout() {
  clearAuth()
  router.push({ name: 'home' })
}
</script>
