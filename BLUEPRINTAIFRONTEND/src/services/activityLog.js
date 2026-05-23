const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getStoredUser() {
  try {
    return JSON.parse(localStorage.getItem("user") || "{}");
  } catch {
    return {};
  }
}

export async function createActivityLog({
  activity_type,
  title,
  description,
  shop_id,
  metadata = {},
}) {
  const user = getStoredUser();

  const payload = {
    user_email: user.email || "unknown@demo.com",
    user_name: user.name || user.teamName || "Demo User",
    shop_id: shop_id || user.shop_id || user.shopId || Number(localStorage.getItem("shop_id")) || 1,
    activity_type,
    title,
    description,
    metadata,
  };

  const res = await fetch(`${API_BASE_URL}/activity-log/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) throw new Error("Failed to save activity log");
  return res.json();
}

export async function getActivityLogs({ activity_type = "all" } = {}) {
  const user = getStoredUser();
  const email = user.email || "unknown@demo.com";
  const shopId = user.shop_id || user.shopId || Number(localStorage.getItem("shop_id")) || 1;

  const params = new URLSearchParams({
    user_email: email,
    shop_id: String(shopId),
    activity_type,
  });

  const res = await fetch(`${API_BASE_URL}/activity-log/?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to load activity logs");
  return res.json();
}

export async function clearActivityLogs() {
  const user = getStoredUser();
  const email = user.email || "unknown@demo.com";
  const shopId = user.shop_id || user.shopId || Number(localStorage.getItem("shop_id")) || 1;

  const params = new URLSearchParams({
    user_email: email,
    shop_id: String(shopId),
  });

  const res = await fetch(`${API_BASE_URL}/activity-log/?${params.toString()}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error("Failed to clear activity logs");
  return res.json();
}
