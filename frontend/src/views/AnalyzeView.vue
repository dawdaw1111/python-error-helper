<template>
  <section class="content-grid analyze-grid">
    <div class="panel-card">
      <div class="panel-head">
        <div>
          <p class="eyebrow">分析结果</p>
          <h2>{{ response?.rule?.title ?? '错误诊断详情' }}</h2>
        </div>
        <button class="ghost-button" type="button" @click="goHome">重新输入</button>
      </div>

      <div class="code-block">{{ currentQuery || '请先从首页输入报错信息。' }}</div>

      <div v-if="loading" class="loading-card">正在匹配规则并生成排查建议...</div>
      <div v-else-if="errorMessage" class="empty-card">
        <strong>请求失败</strong>
        <p>{{ errorMessage }}</p>
      </div>
      <div v-else-if="response" class="result-stack">
        <div class="info-banner">
          <span class="banner-score">匹配度 {{ Math.round(response.confidence * 100) }}%</span>
          <p>{{ response.summary }}</p>
        </div>

        <template v-if="response.rule">
          <section class="section-block">
            <h3>错误解释</h3>
            <p>{{ response.rule.explanation }}</p>
          </section>

          <section class="section-block">
            <h3>常见原因</h3>
            <div class="tag-cloud">
              <span v-for="cause in response.rule.common_causes" :key="cause" class="soft-pill">
                {{ cause }}
              </span>
            </div>
          </section>

          <section class="section-block">
            <h3>排查步骤</h3>
            <ol class="step-list">
              <li v-for="step in response.rule.troubleshooting_steps" :key="step">{{ step }}</li>
            </ol>
          </section>

          <section class="section-block">
            <h3>解决方案</h3>
            <div class="solution-list">
              <div v-for="solution in response.rule.solutions" :key="solution" class="solution-item">
                {{ solution }}
              </div>
            </div>
          </section>

          <section class="section-block">
            <h3>这条结果有帮助吗？</h3>
            <div class="feedback-row">
              <button
                class="ghost-button"
                type="button"
                :disabled="feedbackLoading"
                @click="handleFeedback('helpful')"
              >
                {{ feedbackLoading && feedbackType === 'helpful' ? '提交中...' : '有帮助' }}
              </button>
              <button
                class="primary-button"
                type="button"
                :disabled="feedbackLoading"
                @click="handleFeedback('not_helpful')"
              >
                {{ feedbackLoading && feedbackType === 'not_helpful' ? '提交中...' : '没帮助' }}
              </button>
            </div>
            <p v-if="feedbackMessage" class="inline-note">{{ feedbackMessage }}</p>
          </section>
        </template>
        <template v-else>
          <div class="empty-card">
            <strong>暂未命中现有规则</strong>
            <p>
              可以尝试补充完整 traceback、确认最后一行错误类型，或者前往后台新增一条规则。
            </p>
          </div>
        </template>
      </div>
    </div>

    <aside class="panel-card compact-card">
      <div class="panel-head">
        <div>
          <p class="eyebrow">相关推荐</p>
          <h2>接近的错误规则</h2>
        </div>
      </div>

      <div class="stack-list">
        <button
          v-for="rule in response?.related_rules ?? []"
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
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { analyzeError, submitFeedback } from '../api'
import type { AnalyzeResponse } from '../types'

const route = useRoute()
const router = useRouter()

const response = ref<AnalyzeResponse | null>(null)
const loading = ref(false)
const errorMessage = ref('')
const feedbackLoading = ref(false)
const feedbackType = ref<'helpful' | 'not_helpful' | null>(null)
const feedbackMessage = ref('')

const currentQuery = computed(() => String(route.query.q ?? '').trim())

watch(
  currentQuery,
  async (value) => {
    feedbackMessage.value = ''
    if (!value) {
      response.value = null
      return
    }

    loading.value = true
    errorMessage.value = ''
    try {
      response.value = await analyzeError(value)
    } catch (error) {
      errorMessage.value = error instanceof Error ? error.message : '分析失败，请稍后重试。'
    } finally {
      loading.value = false
    }
  },
  { immediate: true },
)

function goHome() {
  router.push({ name: 'home' })
}

function goAnalyze(value: string) {
  router.push({ name: 'analyze', query: { q: value } })
}

async function handleFeedback(type: 'helpful' | 'not_helpful') {
  if (!response.value?.rule) return

  feedbackLoading.value = true
  feedbackType.value = type
  try {
    const result = await submitFeedback(response.value.rule.id, type)
    feedbackMessage.value = result.message
  } catch (error) {
    feedbackMessage.value = error instanceof Error ? error.message : '反馈提交失败。'
  } finally {
    feedbackLoading.value = false
  }
}
</script>
