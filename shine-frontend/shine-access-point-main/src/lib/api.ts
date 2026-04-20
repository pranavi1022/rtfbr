/**
 * src/lib/api.ts
 *
 * Centralized API configuration.
 * Reads VITE_API_BASE from .env (set in Render dashboard for production).
 * Falls back to the production URL if the variable is not set.
 */

export const API_BASE =
  import.meta.env.VITE_API_BASE || "https://shine-backend-08ll.onrender.com";

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
