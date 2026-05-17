export function logActivity(type, title, description = "", metadata = {}) {
  const currentUser = JSON.parse(localStorage.getItem("demoUser") || "null");
  const shopId = localStorage.getItem("selectedShopId") || "1";

  const newLog = {
    id: Date.now(),
    type,
    title,
    description,
    shop_id: shopId,
    user_email: currentUser?.email || "demo-user",
    user_name: currentUser?.name || "Demo User",
    metadata,
    created_at: new Date().toISOString(),
  };

  const existing = JSON.parse(localStorage.getItem("blueprintActivityLog") || "[]");
  localStorage.setItem("blueprintActivityLog", JSON.stringify([newLog, ...existing]));

  return newLog;
}

export function getActivityLog() {
  return JSON.parse(localStorage.getItem("blueprintActivityLog") || "[]");
}

export function clearActivityLog() {
  localStorage.removeItem("blueprintActivityLog");
}
