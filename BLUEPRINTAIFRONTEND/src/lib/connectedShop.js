export function getConnectedShopId() {
  return localStorage.getItem("connected_shop_id");
}

export function getConnectedShopName() {
  return localStorage.getItem("connected_shop_name") || "No shop connected";
}

export function getConnectedShopCategory() {
  return localStorage.getItem("connected_shop_category") || "";
}

export function setConnectedShop(shop) {
  localStorage.setItem("connected_shop_id", shop.id);
  localStorage.setItem("connected_shop_name", shop.shop_name || shop.name);
  localStorage.setItem("connected_shop_category", shop.category || "");
  localStorage.setItem("connected_shop_region", shop.region || "");
  localStorage.setItem("connected_shop_currency", shop.currency || "USD");
}

export function clearConnectedShop() {
  localStorage.removeItem("connected_shop_id");
  localStorage.removeItem("connected_shop_name");
  localStorage.removeItem("connected_shop_category");
  localStorage.removeItem("connected_shop_region");
  localStorage.removeItem("connected_shop_currency");
}
