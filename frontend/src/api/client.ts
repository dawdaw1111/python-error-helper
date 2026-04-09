const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api'
const ADMIN_TOKEN_KEY = 'pyerr_admin_token'

type RequestInitWithBody = Omit<RequestInit, 'body'> & {
  body?: unknown
}

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

function getStoredToken() {
  return window.localStorage.getItem(ADMIN_TOKEN_KEY)
}

export async function request<T>(
  path: string,
  options: RequestInitWithBody = {},
): Promise<T> {
  const headers = new Headers(options.headers)
  headers.set('Accept', 'application/json')
  const token = getStoredToken()

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  let body = options.body
  if (body && typeof body !== 'string') {
    headers.set('Content-Type', 'application/json')
    body = JSON.stringify(body)
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    body: body as BodyInit | null | undefined,
  })

  if (!response.ok) {
    const contentType = response.headers.get('content-type') ?? ''
    if (contentType.includes('application/json')) {
      const payload = (await response.json()) as { detail?: string }
      throw new ApiError(payload.detail || '请求失败，请稍后重试。', response.status)
    }

    const text = await response.text()
    throw new ApiError(text || '请求失败，请稍后重试。', response.status)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return (await response.json()) as T
}
