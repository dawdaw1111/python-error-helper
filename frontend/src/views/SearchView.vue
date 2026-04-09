<template>
  <section class="content-grid">
    <div class="panel-card">
      <div class="panel-head">
        <div>
          <p class="eyebrow">搜索结果</p>
          <h2>支持中文、英文错误名和模糊搜索</h2>
        </div>
      </div>

      <form class="search-row" @submit.prevent="submitSearch">
        <input
          v-model="keyword"
          class="search-input"
          placeholder="搜索：模块找不到 / ImportError / list index out of range"
        />
        <button class="primary-button" type="submit">搜索</button>
      </form>

      <div class="result-meta">
        <span>关键词：{{ currentKeyword || '热门规则' }}</span>
        <span>{{ loading ? '搜索中...' : `共 ${results.length} 条结果` }}</span>
      </div>

      <div v-if="loading" class="loading-card">正在搜索规则库...</div>
      <div v-else-if="results.length" class="stack-list">
        <button
          v-for="rule in results"
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
            <span v-for="tag in rule.tags" :key="tag" class="tag">{{ tag }}</span>
          </span>
        </button>
      </div>
      <div v-else class="empty-card">
        <strong>没有找到匹配结果</strong>
        <p>可以换一个关键词，或直接把完整报错粘到首页进行分析。</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { searchRules } from '../api'
import type { Rule } from '../types'

const route = useRoute()
const router = useRouter()

const results = ref<Rule[]>([])
const loading = ref(false)
const keyword = ref(String(route.query.q ?? ''))

const currentKeyword = ref(String(route.query.q ?? '').trim())

watch(
  () => route.query.q,
  async (value) => {
    currentKeyword.value = String(value ?? '').trim()
    keyword.value = currentKeyword.value
    loading.value = true
    try {
      const data = await searchRules(currentKeyword.value)
      results.value = data.items
    } catch (error) {
      console.error(error)
      results.value = []
    } finally {
      loading.value = false
    }
  },
  { immediate: true },
)

function submitSearch() {
  router.push({ name: 'search', query: { q: keyword.value.trim() } })
}

function goAnalyze(value: string) {
  router.push({ name: 'analyze', query: { q: value } })
}
</script>
