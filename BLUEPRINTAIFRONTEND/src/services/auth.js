export async function loginWithGoogle(credential) {
  const res = await fetch("http://127.0.0.1:8000/auth/google", {
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
