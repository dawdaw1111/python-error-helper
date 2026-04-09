import { reactive } from 'vue'

import { fetchCurrentAdmin, loginAdmin } from './api'
import { ApiError } from './api/client'

const ADMIN_TOKEN_KEY = 'pyerr_admin_token'
const ADMIN_USERNAME_KEY = 'pyerr_admin_username'

export const authState = reactive({
  token: window.localStorage.getItem(ADMIN_TOKEN_KEY) ?? '',
  username: window.localStorage.getItem(ADMIN_USERNAME_KEY) ?? '',
  initialized: false,
})

function persistAuth(token: string, username: string) {
  window.localStorage.setItem(ADMIN_TOKEN_KEY, token)
  window.localStorage.setItem(ADMIN_USERNAME_KEY, username)
  authState.token = token
  authState.username = username
}

export function clearAuth() {
  window.localStorage.removeItem(ADMIN_TOKEN_KEY)
  window.localStorage.removeItem(ADMIN_USERNAME_KEY)
  authState.token = ''
  authState.username = ''
}

export async function login(username: string, password: string) {
  const result = await loginAdmin(username, password)
  persistAuth(result.access_token, result.username)
  authState.initialized = true
  return result
}

export async function ensureAuthInitialized() {
  if (authState.initialized) return

  if (!authState.token) {
    authState.initialized = true
    return
  }

  try {
    const profile = await fetchCurrentAdmin()
    authState.username = profile.username
  } catch (error) {
    if (error instanceof ApiError && error.status === 401) {
      clearAuth()
    } else {
      throw error
    }
  } finally {
    authState.initialized = true
  }
}

export function isAuthenticated() {
  return Boolean(authState.token)
}
