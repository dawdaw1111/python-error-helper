<template>
  <section class="home-grid">
    <div class="hero-card">
      <p class="eyebrow">PyErr · Python 报错速查</p>
      <h1>Python 报错别乱搜，直接查原因。</h1>
      <p class="hero-copy">
        输入一行异常信息，快速拿到错误解释、排查步骤和修复方案，把排错过程压缩成一次明确的分析。
      </p>

      <form class="hero-form" @submit.prevent="submitQuery">
        <textarea
          v-model="query"
          rows="4"
          placeholder="例如：ModuleNotFoundError: No module named 'requests'"
        />
        <button class="primary-button hero-submit" :disabled="isSubmitting" type="submit">
          {{ isSubmitting ? '正在跳转...' : '开始诊断' }}
        </button>
      </form>

      <div class="chip-group">
        <button
          v-for="prompt in highlights.quick_prompts"
          :key="prompt"
          class="chip-button"
          type="button"
          @click="goSearch(prompt)"
        >
          {{ prompt }}
        </button>
      </div>
    </div>

    <aside class="side-card">
      <div class="side-card-head">
        <div>
          <p class="eyebrow">热门错误</p>
          <h2>先从高频问题下手</h2>
        </div>
        <RouterLink class="text-link" to="/search">查看全部</RouterLink>
      </div>

      <div class="stack-list">
        <button
          v-for="rule in highlights.popular_rules"
          :key="rule.id"
          class="stack-item"
          type="button"
          @click="goAnalyze(rule.example_query)"
        >
          <div>
            <strong>{{ rule.title }}</strong>
            <p>{{ rule.explanation }}</p>
          </div>
          <span class="tag-row">
            <span v-for="tag in rule.tags.slice(0, 2)" :key="tag" class="tag">{{ tag }}</span>
          </span>
        </button>
      </div>
    </aside>

    <section class="value-row">
      <article v-for="item in valueItems" :key="item.title" class="value-card">
        <p class="value-icon">{{ item.icon }}</p>
        <strong>{{ item.title }}</strong>
        <p>{{ item.copy }}</p>
      </article>
    </section>
  </section>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

import { fetchHighlights } from '../api'
import type { HighlightsResponse } from '../types'

const router = useRouter()
const query = ref('')
const isSubmitting = ref(false)
const highlights = reactive<HighlightsResponse>({
  quick_prompts: ['模块找不到', '缩进错误', '类型报错', 'Key 不存在'],
  popular_rules: [],
})

const valueItems = [
  { icon: '◎', title: '一分钟定位原因', copy: '把 traceback 翻译成更容易理解的中文排查路径。' },
  { icon: '◌', title: '标准化修复步骤', copy: '每条结果都包含常见原因、排查动作和可执行方案。' },
  { icon: '◍', title: '持续积累规则库', copy: '后台可直接维护规则、统计命中和反馈表现。' },
]

onMounted(async () => {
  try {
    const data = await fetchHighlights()
    highlights.quick_prompts = data.quick_prompts
    highlights.popular_rules = data.popular_rules
  } catch (error) {
    console.error(error)
  }
})

function goAnalyze(value: string) {
  router.push({ name: 'analyze', query: { q: value } })
}

function goSearch(value: string) {
  router.push({ name: 'search', query: { q: value } })
}

async function submitQuery() {
  const trimmed = query.value.trim()
  if (!trimmed) return

  isSubmitting.value = true
  try {
    await router.push({ name: 'analyze', query: { q: trimmed } })
  } finally {
    isSubmitting.value = false
  }
}
</script>
