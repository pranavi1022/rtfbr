/**
 * src/lib/api.ts
 *
 * Centralized API configuration.
 * Points to the deployed backend on Render.
 */

export const API_BASE = "https://rtfbr.onrender.com";

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
