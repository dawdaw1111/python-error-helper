import type {
  AdminProfile,
  AdminStats,
  AnalyzeResponse,
  AuthResponse,
  HighlightsResponse,
  Rule,
  RulePayload,
  SearchResponse,
} from '../types'
import { request } from './client'

export function fetchHighlights() {
  return request<HighlightsResponse>('/highlights')
}

export function analyzeError(queryText: string) {
  return request<AnalyzeResponse>('/analyze', {
    method: 'POST',
    body: { query_text: queryText },
  })
}

export function searchRules(query: string) {
  return request<SearchResponse>(`/search?q=${encodeURIComponent(query)}`)
}

export function submitFeedback(ruleId: number, feedbackType: 'helpful' | 'not_helpful') {
  return request<{ success: boolean; message: string }>('/feedback', {
    method: 'POST',
    body: { rule_id: ruleId, feedback_type: feedbackType },
  })
}

export function loginAdmin(username: string, password: string) {
  return request<AuthResponse>('/auth/login', {
    method: 'POST',
    body: { username, password },
  })
}

export function fetchCurrentAdmin() {
  return request<AdminProfile>('/auth/me')
}

export async function fetchAdminRules() {
  const response = await request<{ items: Rule[] }>('/admin/rules')
  return response.items
}

export function fetchAdminStats() {
  return request<AdminStats>('/admin/stats')
}

export function createRule(payload: RulePayload) {
  return request<Rule>('/admin/rules', { method: 'POST', body: payload })
}

export function updateRule(ruleId: number, payload: RulePayload) {
  return request<Rule>(`/admin/rules/${ruleId}`, { method: 'PUT', body: payload })
}

export function deleteRule(ruleId: number) {
  return request<void>(`/admin/rules/${ruleId}`, { method: 'DELETE' })
}
