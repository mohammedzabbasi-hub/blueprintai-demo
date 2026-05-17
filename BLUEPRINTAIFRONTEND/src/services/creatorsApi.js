const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getAuthHeaders() {
  const token =
    localStorage.getItem("token") ||
    localStorage.getItem("access_token");

  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

function getConnectedShopId() {
  return localStorage.getItem("connected_shop_id");
}

function withShopId(path) {
  const shopId = getConnectedShopId();

  if (!shopId) {
    throw new Error("No TikTok Shop connected. Please connect a demo shop first.");
  }

  const separator = path.includes("?") ? "&" : "?";
  return `${path}${separator}shop_id=${shopId}`;
}

async function handleResponse(response) {
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText || "Creator API request failed");
  }

  return response.json();
}

export async function getCreators() {
  const response = await fetch(`${API_BASE_URL}${withShopId("/creators/")}`, {
    headers: getAuthHeaders(),
  });

  return handleResponse(response);
}

export async function getCreatorById(creatorId) {
  const response = await fetch(`${API_BASE_URL}/creators/${creatorId}`, {
    headers: getAuthHeaders(),
  });

  return handleResponse(response);
}

export async function createCreator(creatorData) {
  const shopId = getConnectedShopId();

  const response = await fetch(`${API_BASE_URL}/creators/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify({
      ...creatorData,
      brand_id: creatorData.brand_id || shopId,
    }),
  });

  return handleResponse(response);
}

export async function updateCreator(creatorId, creatorData) {
  const response = await fetch(`${API_BASE_URL}/creators/${creatorId}`, {
    method: "PUT",
    headers: getAuthHeaders(),
    body: JSON.stringify(creatorData),
  });

  return handleResponse(response);
}

export async function deleteCreator(creatorId) {
  const response = await fetch(`${API_BASE_URL}/creators/${creatorId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });

  return handleResponse(response);
}

export async function getCreatorComparison() {
  const response = await fetch(
    `${API_BASE_URL}${withShopId("/creators/compare")}`,
    {
      headers: getAuthHeaders(),
    }
  );

  return handleResponse(response);
}
