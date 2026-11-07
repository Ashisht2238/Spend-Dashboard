const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function getJson(path, filters = {}) {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filters)) {
    if (value) {
      params.append(key, value);
    }
  }
  const query = params.toString();
  const url = `${API_URL}${path}${query ? `?${query}` : ""}`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}