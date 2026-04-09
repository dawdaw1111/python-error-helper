export interface Rule {
  id: number
  title: string
  error_type: string
  pattern_type: 'regex' | 'exact' | 'contains'
  pattern_value: string
  example_query: string
  explanation: string
  common_causes: string[]
  troubleshooting_steps: string[]
  solutions: string[]
  tags: string[]
  search_terms: string[]
  created_at: string
}

export interface AnalyzeResponse {
  query_text: string
  extracted_error_type: string | null
  matched: boolean
  match_type: string
  confidence: number
  summary: string
  rule: Rule | null
  related_rules: Rule[]
}

export interface SearchResponse {
  query: string
  total: number
  items: Rule[]
}

export interface HighlightsResponse {
  quick_prompts: string[]
  popular_rules: Rule[]
}

export interface AdminStats {
  total_queries: number
  matched_queries: number
  unmatched_queries: number
  matched_rate: number
  total_feedback: number
  helpful_feedback: number
  helpful_rate: number
  top_rules: Array<{
    rule_id: number
    title: string
    hits: number
  }>
}

export interface RulePayload {
  title: string
  error_type: string
  pattern_type: 'regex' | 'exact' | 'contains'
  pattern_value: string
  example_query: string
  explanation: string
  common_causes: string[]
  troubleshooting_steps: string[]
  solutions: string[]
  tags: string[]
  search_terms: string[]
}

export interface AuthResponse {
  access_token: string
  token_type: 'bearer'
  username: string
  expires_in: number
}

export interface AdminProfile {
  username: string
}
