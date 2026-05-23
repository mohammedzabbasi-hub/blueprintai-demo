const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function safeJsonParse(value) {
  try {
    return value ? JSON.parse(value) : null;
  } catch {
    return null;
  }
}

function getStoredUser() {
  const possibleUserKeys = [
    "user",
    "currentUser",
    "demoUser",
    "authUser",
    "blueprint_user",
    "selectedUser",
  ];

  for (const key of possibleUserKeys) {
    const parsed = safeJsonParse(localStorage.getItem(key));
    if (parsed && (parsed.email || parsed.user_email)) return parsed;
  }

  return {};
}

function getSelectedShopId() {
  const possibleShopKeys = [
    "selectedShopId",
    "shop_id",
    "shopId",
    "currentShopId",
    "demoShopId",
    "connectedShopId",
  ];

  for (const key of possibleShopKeys) {
    const value = localStorage.getItem(key);
    if (value && !Number.isNaN(Number(value))) return Number(value);
  }

  const user = getStoredUser();
  return Number(user.shop_id || user.shopId || user.selected_shop_id || 1);
}

function getActivityContext() {
  const user = getStoredUser();
  const shopId = getSelectedShopId();

  return {
    user_email:
      user.email ||
      user.user_email ||
      user.username ||
      localStorage.getItem("email") ||
      "unknown@demo.com",
    user_name:
      user.name ||
      user.user_name ||
      user.teamName ||
      user.team_name ||
      user.displayName ||
      "Demo User",
    shop_id: shopId,
  };
}

export async function createActivityLog(activity) {
  const context = getActivityContext();

  const payload = {
    user_email: activity.user_email || context.user_email,
    user_name: activity.user_name || context.user_name,
    shop_id: activity.shop_id || context.shop_id,
    activity_type: activity.activity_type || "general",
    title: activity.title || "Activity",
    description: activity.description || "",
    metadata: activity.metadata || {},
  };

  const res = await fetch(`${API_BASE}/activity-log/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`Failed to create activity log: ${res.status}`);
  }

  return res.json();
}

export async function getActivityLogs(options = {}) {
  const context = getActivityContext();

  const params = new URLSearchParams();
  params.set("user_email", options.user_email || context.user_email);
  params.set("shop_id", options.shop_id || context.shop_id);

  if (options.activity_type && options.activity_type !== "all") {
    params.set("activity_type", options.activity_type);
  }

  const res = await fetch(`${API_BASE}/activity-log/?${params.toString()}`);

  if (!res.ok) {
    throw new Error(`Failed to fetch activity logs: ${res.status}`);
  }

  return res.json();
}

export async function clearActivityLogs(options = {}) {
  const context = getActivityContext();

  const params = new URLSearchParams();
  params.set("user_email", options.user_email || context.user_email);
  params.set("shop_id", options.shop_id || context.shop_id);

  const res = await fetch(`${API_BASE}/activity-log/?${params.toString()}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    throw new Error(`Failed to clear activity logs: ${res.status}`);
  }

  return res.json();
}

// Backward-compatible names used by existing pages
export async function logActivity(activity) {
  return createActivityLog(activity);
}

export async function getActivityLog(options = {}) {
  return getActivityLogs(options);
}

export async function clearActivityLog(options = {}) {
  return clearActivityLogs(options);
}
