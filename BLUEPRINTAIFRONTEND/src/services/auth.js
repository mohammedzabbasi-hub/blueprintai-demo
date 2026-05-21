const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function loginWithGoogle(credential) {
  const res = await fetch(`${API_BASE}/auth/google`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ credential }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Google login failed");
  }

  return data;
}
