<template>
  <div v-if="open" class="drawer-backdrop" @click.self="$emit('close')">
    <aside class="drawer-panel">
      <div class="drawer-head">
        <div>
          <p class="eyebrow">{{ mode === 'create' ? '新增规则' : '编辑规则' }}</p>
          <h3>{{ mode === 'create' ? '补充新的 Python 错误规则' : '调整已有规则内容' }}</h3>
        </div>
        <button class="ghost-button" type="button" @click="$emit('close')">关闭</button>
      </div>

      <form class="drawer-form" @submit.prevent="handleSubmit">
        <label>
          <span>标题</span>
          <input v-model.trim="form.title" required placeholder="如：ModuleNotFoundError：找不到模块" />
        </label>

        <div class="field-grid">
          <label>
            <span>错误类型</span>
            <input v-model.trim="form.error_type" required placeholder="ModuleNotFoundError" />
          </label>
          <label>
            <span>匹配方式</span>
            <select v-model="form.pattern_type">
              <option value="regex">regex</option>
              <option value="exact">exact</option>
              <option value="contains">contains</option>
            </select>
          </label>
        </div>

        <label>
          <span>匹配表达式</span>
          <input v-model.trim="form.pattern_value" required placeholder="例如：ModuleNotFoundError:" />
        </label>

        <label>
          <span>示例报错</span>
          <textarea
            v-model.trim="form.example_query"
            rows="3"
            required
            placeholder="ModuleNotFoundError: No module named 'requests'"
          />
        </label>

        <label>
          <span>错误解释</span>
          <textarea v-model.trim="form.explanation" rows="4" required />
        </label>

        <label>
          <span>常见原因</span>
          <textarea
            v-model="text.common_causes"
            rows="4"
            placeholder="每行一条"
          />
        </label>

        <label>
          <span>排查步骤</span>
          <textarea
            v-model="text.troubleshooting_steps"
            rows="4"
            placeholder="每行一条"
          />
        </label>

        <label>
          <span>解决方案</span>
          <textarea v-model="text.solutions" rows="4" placeholder="每行一条" />
        </label>

        <label>
          <span>标签</span>
          <input v-model="text.tags" placeholder="使用逗号分隔，如 Python, Import, 环境问题" />
        </label>

        <label>
          <span>搜索词</span>
          <input v-model="text.search_terms" placeholder="使用逗号分隔，如 模块找不到, no module named" />
        </label>

        <div class="drawer-actions">
          <button class="ghost-button" type="button" @click="$emit('close')">取消</button>
          <button class="primary-button" :disabled="submitting" type="submit">
            {{ submitting ? '保存中...' : '保存规则' }}
          </button>
        </div>
      </form>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

import type { Rule, RulePayload } from '../types'

const props = defineProps<{
  open: boolean
  mode: 'create' | 'edit'
  rule: Rule | null
  submitting: boolean
}>()

const emit = defineEmits<{
  close: []
  submit: [payload: RulePayload]
}>()

const createDefaultForm = (): RulePayload => ({
  title: '',
  error_type: '',
  pattern_type: 'regex',
  pattern_value: '',
  example_query: '',
  explanation: '',
  common_causes: [],
  troubleshooting_steps: [],
  solutions: [],
  tags: [],
  search_terms: [],
})

const form = reactive<RulePayload>(createDefaultForm())
const text = reactive({
  common_causes: '',
  troubleshooting_steps: '',
  solutions: '',
  tags: '',
  search_terms: '',
})

function normalizeLines(value: string) {
  return value
    .split('\n')
    .map((item) => item.trim())
    .filter(Boolean)
}

function normalizeTags(value: string) {
  return value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
}

function syncForm(rule: Rule | null) {
  const source = rule ?? createDefaultForm()
  form.title = source.title
  form.error_type = source.error_type
  form.pattern_type = source.pattern_type
  form.pattern_value = source.pattern_value
  form.example_query = source.example_query
  form.explanation = source.explanation
  form.common_causes = [...source.common_causes]
  form.troubleshooting_steps = [...source.troubleshooting_steps]
  form.solutions = [...source.solutions]
  form.tags = [...source.tags]
  form.search_terms = [...source.search_terms]
  text.common_causes = source.common_causes.join('\n')
  text.troubleshooting_steps = source.troubleshooting_steps.join('\n')
  text.solutions = source.solutions.join('\n')
  text.tags = source.tags.join(', ')
  text.search_terms = source.search_terms.join(', ')
}

watch(
  () => [props.open, props.rule],
  () => {
    if (props.open) {
      syncForm(props.rule)
    }
  },
  { immediate: true },
)

function handleSubmit() {
  emit('submit', {
    ...form,
    common_causes: normalizeLines(text.common_causes),
    troubleshooting_steps: normalizeLines(text.troubleshooting_steps),
    solutions: normalizeLines(text.solutions),
    tags: normalizeTags(text.tags),
    search_terms: normalizeTags(text.search_terms),
  })
}
</script>
