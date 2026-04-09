<template>
  <section class="login-shell">
    <div class="login-card">
      <p class="eyebrow">管理员登录</p>
      <h1>登录后才能进入后台规则配置。</h1>
      <p class="hero-copy">
        后台页面已从公开导航中移除。请输入管理员账号和密码，通过后可维护规则、查看统计并调整匹配策略。
      </p>

      <form class="login-form" @submit.prevent="submitLogin">
        <label>
          <span>账号</span>
          <input v-model.trim="form.username" autocomplete="username" placeholder="请输入管理员账号" />
        </label>

        <label>
          <span>密码</span>
          <input
            v-model="form.password"
            autocomplete="current-password"
            placeholder="请输入管理员密码"
            type="password"
          />
        </label>

        <button class="primary-button login-submit" :disabled="submitting" type="submit">
          {{ submitting ? '登录中...' : '登录后台' }}
        </button>
      </form>

      <p v-if="errorMessage" class="login-error">{{ errorMessage }}</p>
      <p class="login-help">管理员账号密码由后端环境变量配置。</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { login } from '../auth'

const route = useRoute()
const router = useRouter()

const form = reactive({
  username: '',
  password: '',
})
const submitting = ref(false)
const errorMessage = ref('')

async function submitLogin() {
  const username = form.username.trim()
  const password = form.password

  if (!username || !password) {
    errorMessage.value = '请输入账号和密码。'
    return
  }

  submitting.value = true
  errorMessage.value = ''
  try {
    await login(username, password)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/admin'
    await router.push(redirect)
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '登录失败，请稍后重试。'
  } finally {
    submitting.value = false
  }
}
</script>
