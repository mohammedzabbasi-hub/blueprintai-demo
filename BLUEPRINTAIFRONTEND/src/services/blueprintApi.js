const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getAuthHeaders() {
  const token =
    localStorage.getItem("token") ||
    localStorage.getItem("access_token") ||
    localStorage.getItem("authToken");

  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function getLatestBlueprint(shopId = 1) {
  const res = await fetch(`${API_BASE}/blueprint/${shopId}/latest`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch latest blueprint");
  }

  return res.json();
}

export async function generateBlueprint(shopId = 1) {
  const res = await fetch(`${API_BASE}/blueprint/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ shop_id: shopId }),
  });

  if (!res.ok) {
    throw new Error("Failed to generate blueprint");
  }

  return res.json();
}

export async function completeBlueprintStep(stepId, isCompleted = true) {
  const res = await fetch(`${API_BASE}/blueprint/complete-step`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
    },
    body: JSON.stringify({
      step_id: stepId,
      is_completed: isCompleted,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to update blueprint step");
  }

  return res.json();
}
