export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

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

export function getAuthHeaders(json = false) {
  const token =
    localStorage.getItem("token") ||
    localStorage.getItem("access_token") ||
    localStorage.getItem("authToken");

  return {
    ...(json ? { "Content-Type": "application/json" } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export function getSelectedShopId() {
  const user = getCurrentUser();
  const shop = getSelectedShop();
  const userScopedShopId = user.id
    ? localStorage.getItem(`selectedShopId:${user.id}`)
    : null;

  return Number(
    userScopedShopId ||
      shop.id ||
      shop.shop_id ||
      localStorage.getItem("selectedShopId") ||
      localStorage.getItem("shop_id") ||
      localStorage.getItem("connected_shop_id") ||
      user.shop_id ||
      user.shopId ||
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

export function setSelectedShop(shop) {
  const id = String(shop.id || shop.shop_id || shop.shopId || "");
  if (!id) return;

  const normalizedShop = {
    ...shop,
    id: Number.isNaN(Number(id)) ? id : Number(id),
    shop_id: Number.isNaN(Number(id)) ? id : Number(id),
    shop_name: shop.shop_name || shop.name || "Selected Shop",
    name: shop.name || shop.shop_name || "Selected Shop",
  };

  localStorage.setItem("selectedShop", JSON.stringify(normalizedShop));
  localStorage.setItem("selectedShopId", id);
  localStorage.setItem("shop_id", id);
  localStorage.setItem("connected_shop_id", id);
  localStorage.setItem("selectedShopName", normalizedShop.shop_name);
  localStorage.setItem("connected_shop_name", normalizedShop.shop_name);
  localStorage.setItem("connected_shop_category", shop.category || "");
  localStorage.setItem("connected_shop_region", shop.region || "");
  localStorage.setItem("connected_shop_currency", shop.currency || "USD");

  const user = getCurrentUser();
  if (user.id) {
    localStorage.setItem(`selectedShopId:${user.id}`, id);
  }

  window.dispatchEvent(
    new CustomEvent("blueprintai:shop-changed", {
      detail: { shopId: id, shop: normalizedShop },
    })
  );
}
