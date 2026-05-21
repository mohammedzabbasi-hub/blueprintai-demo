const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export function getSelectedShopId() {
  const rawUser = localStorage.getItem("demoUser");

  if (rawUser) {
    try {
      const user = JSON.parse(rawUser);
      const userShop = localStorage.getItem(`selectedShopId:${user.id}`);
      if (userShop) return userShop;
      if (user.defaultShopId) return String(user.defaultShopId);
    } catch {}
  }

  return (
    localStorage.getItem("selectedShopId") ||
    localStorage.getItem("shop_id") ||
    localStorage.getItem("demoShopId") ||
    localStorage.getItem("connected_shop_id") ||
    "1"
  );
}

async function request(path) {
  const res = await fetch(`${API_BASE}${path}`);
  const data = await res.json().catch(() => null);

  if (!res.ok) {
    throw new Error(data?.detail || `Request failed: ${res.status}`);
  }

  return data;
}

export async function getEngineAnalysis(shopId = getSelectedShopId()) {
  const data = await request(`/analytics/dashboard?shop_id=${encodeURIComponent(shopId)}`);

  return {
    ...data,
    shop_id: data.shop?.id || shopId,
    shop_name: data.shop?.shop_name || data.shop?.name || "BluePrintAI",
    scored_creatives: data.leaderboard || [],
    recommendations: data.recommendations || [],
    next_actions: data.next_actions || data.recommendations || [],
    strategy: data.strategy || {
      recommendations: data.recommendations || data.next_actions || [],
    },
  };
}

export async function getEngineRecommendations(shopId = getSelectedShopId()) {
  return request(`/recommendations?shop_id=${encodeURIComponent(shopId)}`);
}

export async function getEngineBriefs(shopId = getSelectedShopId(), productName = "") {
  const productQuery = productName ? `&product_name=${encodeURIComponent(productName)}` : "";
  return request(`/briefs?shop_id=${encodeURIComponent(shopId)}${productQuery}`);
}

export async function getGeminiStrategy(shopId = getSelectedShopId(), productName = "") {
  const productQuery = productName ? `&product_name=${encodeURIComponent(productName)}` : "";
  return request(`/analytics/dashboard?shop_id=${encodeURIComponent(shopId)}${productQuery}`);
}
