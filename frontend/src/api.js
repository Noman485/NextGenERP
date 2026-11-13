import { API_BASE_URL } from './config';

const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const NO_REFRESH_PATHS = new Set([
  '/auth/login',
  '/auth/register',
  '/auth/refresh',
  '/auth/logout',
]);

let refreshPromise = null;

export function getAccessToken() {
  return sessionStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken() {
  return sessionStorage.getItem(REFRESH_TOKEN_KEY);
}

export function setSessionTokens(accessToken, refreshToken) {
  if (accessToken) {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  }
  if (refreshToken) {
    sessionStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  } else {
    sessionStorage.removeItem(REFRESH_TOKEN_KEY);
  }
}

export function clearSessionTokens() {
  sessionStorage.removeItem(ACCESS_TOKEN_KEY);
  sessionStorage.removeItem(REFRESH_TOKEN_KEY);
}

async function refreshAccessToken() {
  const refreshToken = getRefreshToken();
  if (!refreshToken) return null;

  if (!refreshPromise) {
    refreshPromise = (async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refreshToken }),
        });
        if (!response.ok) return null;
        const data = await response.json().catch(() => null);
        if (!data?.access_token || !data?.refresh_token) return null;
        setSessionTokens(data.access_token, data.refresh_token);
        return data.access_token;
      } catch {
        return null;
      } finally {
        refreshPromise = null;
      }
    })();
  }

  return refreshPromise;
}

function expired() {
  clearSessionTokens();
  window.dispatchEvent(new Event('auth:expired'));
}

export async function logoutSession() {
  const refreshToken = getRefreshToken();
  clearSessionTokens();
  if (!refreshToken) return;
  try {
    await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
  } catch {
    // The local session is already cleared; a failed revoke call must not
    // keep the user signed in on this device.
  }
}

export async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers);
  const token = getAccessToken();

  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  let response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (response.status !== 401 || !token || NO_REFRESH_PATHS.has(path)) {
    return response;
  }

  const renewedToken = await refreshAccessToken();
  if (!renewedToken) {
    expired();
    return response;
  }

  const retryHeaders = new Headers(options.headers);
  retryHeaders.set('Authorization', `Bearer ${renewedToken}`);
  response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: retryHeaders,
  });

  if (response.status === 401) {
    expired();
  }

  return response;
}
