/**
 * src/lib/api.ts
 *
 * Centralized API configuration.
 * Uses VITE_API_URL from .env (defaults to localhost:5000 for dev).
 */

export const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";

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
