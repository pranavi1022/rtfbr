/**
 * src/lib/api.ts
 *
 * Centralized API configuration.
 *
 * Reads VITE_API_BASE (preferred) or VITE_API_URL from .env.
 * Falls back to "" (same-origin) if neither is set.
 */

export const API_BASE: string =
  import.meta.env.VITE_API_BASE ||
  import.meta.env.VITE_API_URL  ||
  "";

if (!API_BASE) {
  console.warn("API_BASE is not configured. API requests will be made to the same origin.");
}

/**
 * Shorthand for fetch with JSON + credentials.
 */
export async function apiFetch(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", ...options.headers },
    credentials: "include",
    ...options,
  });
  return res;
}
