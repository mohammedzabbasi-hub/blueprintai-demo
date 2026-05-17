export const DEMO_ACCOUNTS = [
  {
    id: "acct_beauty",
    name: "GlowLab Beauty Team",
    email: "beauty@demo.com",
    password: "demo123",
    allowedShopIds: [1],
    defaultShopId: 1,
  },
  {
    id: "acct_fitness",
    name: "FitPulse Gear Team",
    email: "fitness@demo.com",
    password: "demo123",
    allowedShopIds: [2],
    defaultShopId: 2,
  },
  {
    id: "acct_home",
    name: "HomeEase Finds Team",
    email: "home@demo.com",
    password: "demo123",
    allowedShopIds: [3],
    defaultShopId: 3,
  },
  {
    id: "acct_agency",
    name: "BlueprintAI Agency Demo",
    email: "agency@demo.com",
    password: "demo123",
    allowedShopIds: [1, 2, 3, 4, 5],
    defaultShopId: 1,
  },
];

export function loginDemoAccount(email, password) {
  const account = DEMO_ACCOUNTS.find(
    (user) =>
      user.email.toLowerCase() === email.toLowerCase() &&
      user.password === password
  );

  if (!account) {
    throw new Error("Invalid demo login. Try beauty@demo.com / demo123");
  }

  localStorage.setItem("demoUser", JSON.stringify(account));
  localStorage.setItem("isAuthenticated", "true");

  const shopKey = `selectedShopId:${account.id}`;
  const savedShop = localStorage.getItem(shopKey);
  const selectedShopId = savedShop || String(account.defaultShopId);

  localStorage.setItem("selectedShopId", selectedShopId);
  localStorage.setItem(shopKey, selectedShopId);

  return account;
}

export function getCurrentDemoUser() {
  const raw = localStorage.getItem("demoUser");
  if (!raw) return null;

  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function logoutDemoAccount() {
  localStorage.removeItem("demoUser");
  localStorage.removeItem("isAuthenticated");
  localStorage.removeItem("selectedShopId");
  window.location.href = "/login";
}

export function userCanAccessShop(shopId) {
  const user = getCurrentDemoUser();
  if (!user) return true;
  return user.allowedShopIds.includes(Number(shopId));
}

export function setUserSelectedShop(shopId) {
  const user = getCurrentDemoUser();
  localStorage.setItem("selectedShopId", String(shopId));

  if (user) {
    localStorage.setItem(`selectedShopId:${user.id}`, String(shopId));
  }
}
