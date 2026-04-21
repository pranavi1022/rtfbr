/**
 * src/lib/api.ts
 *
 * Centralized API configuration.
 * 
 * IMPORTANT: The correct production backend is shine-backend-08ll.onrender.com.
 * The old rtfbr.onrender.com backend does NOT have PostgreSQL configured.
 * We hardcode the correct URL here because Render's VITE_API_BASE env var
 * may still point to the old URL.
 * 
 * For local development, set VITE_API_BASE=http://localhost:5000 in .env
 */

export const API_BASE =
  import.meta.env.VITE_API_BASE?.includes("localhost")
    ? import.meta.env.VITE_API_BASE
    : "https://shine-backend-08ll.onrender.com";

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
