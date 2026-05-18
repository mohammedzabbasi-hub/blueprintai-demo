export const SHOP_STORAGE_KEY = "selectedShopId";

export function getCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem("demoUser") || "null");
  } catch {
    return null;
  }
}

export function getSelectedShopId() {
  const user = getCurrentUser();

  if (user?.id) {
    const userShopId = localStorage.getItem(`selectedShopId:${user.id}`);
    if (userShopId) return userShopId;
  }

  return (
    localStorage.getItem("selectedShopId") ||
    localStorage.getItem("shop_id") ||
    localStorage.getItem("demoShopId") ||
    localStorage.getItem("connected_shop_id") ||
    "1"
  );
}

export function setSelectedShop(shop) {
  const id = String(shop.id || shop.shop_id || shop.shopId);

  localStorage.setItem("selectedShopId", id);
  localStorage.setItem("shop_id", id);
  localStorage.setItem("connected_shop_id", id);

  localStorage.setItem("selectedShopName", shop.shop_name || shop.name || "Selected Shop");
  localStorage.setItem("connected_shop_name", shop.shop_name || shop.name || "Selected Shop");
  localStorage.setItem("connected_shop_category", shop.category || "");
  localStorage.setItem("connected_shop_region", shop.region || "");
  localStorage.setItem("connected_shop_currency", shop.currency || "USD");

  const user = getCurrentUser();
  if (user?.id) {
    localStorage.setItem(`selectedShopId:${user.id}`, id);
  }

  window.dispatchEvent(new CustomEvent("blueprintai:shop-changed", { detail: { shopId: id, shop } }));
}

export function getStoredShopName() {
  return (
    localStorage.getItem("selectedShopName") ||
    localStorage.getItem("connected_shop_name") ||
    "Select shop"
  );
}
