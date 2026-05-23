export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "https://blueprintai-hvgq.onrender.com";

export const DEMO_EMAILS = new Set([
  "beauty@demo.com",
  "fitness@demo.com",
  "home@demo.com",
  "agency@demo.com",
]);

export function safeJsonParse(value, fallback = {}) {
  try {
    return value ? JSON.parse(value) : fallback;
  } catch {
    return fallback;
  }
}

export function getCurrentUser() {
  return safeJsonParse(localStorage.getItem("user"), {});
}

export function getSelectedShop() {
  return safeJsonParse(localStorage.getItem("selectedShop"), {});
}

export function getSelectedShopId() {
  const user = getCurrentUser();
  const shop = getSelectedShop();

  return Number(
    user.shop_id ||
      user.shopId ||
      shop.id ||
      shop.shop_id ||
      localStorage.getItem("selectedShopId") ||
      localStorage.getItem("shop_id") ||
      1
  );
}

export function isDemoAccount() {
  const user = getCurrentUser();
  const email = String(user.email || "").toLowerCase();

  return user.is_demo === true || DEMO_EMAILS.has(email);
}

export function getAccountLabel() {
  const user = getCurrentUser();
  const shop = getSelectedShop();

  return {
    userName: user.name || "User",
    email: user.email || "",
    shopName: shop.shop_name || shop.name || user.shop_name || "My TikTok Shop",
    shopId: getSelectedShopId(),
    isDemo: isDemoAccount(),
  };
}
