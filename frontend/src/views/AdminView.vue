<template>
  <section class="admin-layout">
    <div class="panel-card admin-banner">
      <div>
        <p class="eyebrow">管理员后台</p>
        <h2>登录后维护规则库与命中策略</h2>
      </div>
      <div class="admin-banner-actions">
        <span class="admin-user">{{ authState.username }}</span>
        <button class="ghost-button" type="button" @click="logoutAdmin">退出登录</button>
      </div>
    </div>

    <div class="stats-grid">
      <article class="metric-card">
        <span>总查询</span>
        <strong>{{ stats.total_queries }}</strong>
        <p>累计进入分析接口的请求数</p>
      </article>
      <article class="metric-card">
        <span>命中率</span>
        <strong>{{ Math.round(stats.matched_rate * 100) }}%</strong>
        <p>{{ stats.matched_queries }} / {{ stats.total_queries || 0 }} 命中规则</p>
      </article>
      <article class="metric-card">
        <span>有帮助率</span>
        <strong>{{ Math.round(stats.helpful_rate * 100) }}%</strong>
        <p>{{ stats.helpful_feedback }} / {{ stats.total_feedback || 0 }} 正向反馈</p>
      </article>
      <article class="metric-card">
        <span>未命中</span>
        <strong>{{ stats.unmatched_queries }}</strong>
        <p>建议优先补充这些空白规则</p>
      </article>
    </div>

    <div class="content-grid">
      <div class="panel-card">
        <div class="panel-head">
          <div>
            <p class="eyebrow">规则管理</p>
            <h2>维护错误库与匹配表达式</h2>
          </div>
          <button class="primary-button" type="button" @click="openCreate">新增规则</button>
        </div>

        <div class="search-row">
          <input
            v-model="filterText"
            class="search-input"
            placeholder="筛选标题、错误类型、标签"
          />
        </div>

        <div v-if="loadError" class="empty-card">
          <strong>后台数据加载失败</strong>
          <p>{{ loadError }}</p>
        </div>

        <div v-else class="stack-list">
          <article v-for="rule in filteredRules" :key="rule.id" class="admin-rule-card">
            <div class="admin-rule-copy">
              <div class="admin-rule-top">
                <strong>{{ rule.title }}</strong>
                <span class="tiny-tag">{{ rule.pattern_type }}</span>
              </div>
              <p>{{ rule.explanation }}</p>
              <div class="tag-row">
                <span v-for="tag in rule.tags" :key="tag" class="tag">{{ tag }}</span>
              </div>
            </div>
            <div class="admin-rule-actions">
              <button class="ghost-button" type="button" @click="openEdit(rule)">编辑</button>
              <button
                class="danger-button"
                :disabled="removingId === rule.id"
                type="button"
                @click="removeRule(rule)"
              >
                {{ removingId === rule.id ? '删除中...' : '删除' }}
              </button>
            </div>
          </article>
        </div>
      </div>

      <aside class="panel-card compact-card">
        <div class="panel-head">
          <div>
            <p class="eyebrow">命中排行</p>
            <h2>最常命中的错误</h2>
          </div>
        </div>

        <div class="ranking-list">
          <div v-for="item in stats.top_rules" :key="item.rule_id" class="ranking-item">
            <div>
              <strong>{{ item.title }}</strong>
              <p>规则 ID #{{ item.rule_id }}</p>
            </div>
            <span>{{ item.hits }}</span>
          </div>
          <div v-if="!stats.top_rules.length" class="empty-card">
            <strong>还没有统计数据</strong>
            <p>跑几次分析和反馈后，这里会展示命中排行。</p>
          </div>
        </div>
      </aside>
    </div>

    <RuleEditorDrawer
      :mode="editor.mode"
      :open="editor.open"
      :rule="editor.rule"
      :submitting="saving"
      @close="closeEditor"
      @submit="saveRule"
    />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import { authState, clearAuth } from '../auth'
import {
  createRule,
  deleteRule,
  fetchAdminRules,
  fetchAdminStats,
  updateRule,
} from '../api'
import { ApiError } from '../api/client'
import RuleEditorDrawer from '../components/RuleEditorDrawer.vue'
import type { AdminStats, Rule, RulePayload } from '../types'

const router = useRouter()
const rules = ref<Rule[]>([])
const filterText = ref('')
const saving = ref(false)
const removingId = ref<number | null>(null)
const loadError = ref('')

const stats = reactive<AdminStats>({
  total_queries: 0,
  matched_queries: 0,
  unmatched_queries: 0,
  matched_rate: 0,
  total_feedback: 0,
  helpful_feedback: 0,
  helpful_rate: 0,
  top_rules: [],
})

const editor = reactive<{
  open: boolean
  mode: 'create' | 'edit'
  rule: Rule | null
}>({
  open: false,
  mode: 'create',
  rule: null,
})

const filteredRules = computed(() => {
  const keyword = filterText.value.trim().toLowerCase()
  if (!keyword) return rules.value

  return rules.value.filter((rule) => {
    return [rule.title, rule.error_type, rule.tags.join(' '), rule.explanation]
      .join(' ')
      .toLowerCase()
      .includes(keyword)
  })
})

onMounted(async () => {
  await refresh()
})

async function refresh() {
  loadError.value = ''
  try {
    const [ruleItems, statItems] = await Promise.all([fetchAdminRules(), fetchAdminStats()])
    rules.value = ruleItems
    Object.assign(stats, statItems)
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      clearAuth()
      await router.push({ name: 'login', query: { redirect: '/admin' } })
      return
    }

    loadError.value = error instanceof Error ? error.message : '加载后台数据失败。'
  }
}

function openCreate() {
  editor.open = true
  editor.mode = 'create'
  editor.rule = null
}

function openEdit(rule: Rule) {
  editor.open = true
  editor.mode = 'edit'
  editor.rule = rule
}

function closeEditor() {
  editor.open = false
}

async function saveRule(payload: RulePayload) {
  saving.value = true
  try {
    if (editor.mode === 'create') {
      await createRule(payload)
    } else if (editor.rule) {
      await updateRule(editor.rule.id, payload)
    }
    await refresh()
    closeEditor()
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      clearAuth()
      await router.push({ name: 'login', query: { redirect: '/admin' } })
      return
    }

    window.alert(error instanceof Error ? error.message : '保存规则失败。')
  } finally {
    saving.value = false
  }
}

async function removeRule(rule: Rule) {
  const confirmed = window.confirm(`确认删除规则「${rule.title}」吗？`)
  if (!confirmed) return

  removingId.value = rule.id
  try {
    await deleteRule(rule.id)
    await refresh()
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      clearAuth()
      await router.push({ name: 'login', query: { redirect: '/admin' } })
      return
    }

    window.alert(error instanceof Error ? error.message : '删除规则失败。')
  } finally {
    removingId.value = null
  }
}

function logoutAdmin() {
  clearAuth()
  router.push({ name: 'login' })
}
</script>
