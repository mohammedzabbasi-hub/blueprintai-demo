export const dashboardStats = {
  revenue: 12450,
  orders: 318,
  conversionRate: 3.8,
  avgOrderValue: 39.15,
};

export const recentPerformance = [
  { date: "Mon", views: 12000, clicks: 410, orders: 52 },
  { date: "Tue", views: 9800, clicks: 360, orders: 44 },
  { date: "Wed", views: 14100, clicks: 470, orders: 61 },
  { date: "Thu", views: 11000, clicks: 390, orders: 49 },
  { date: "Fri", views: 15800, clicks: 520, orders: 72 },
];

export const mockCreatives = [
  {
    id: 1,
    title: "3-second acne fix demo",
    product: "GlowPatch",
    creator: "Ava Lee",
    hook_type: "problem-solution",
    creator_type: "ugc creator",
    score: 91,
  },
  {
    id: 2,
    title: "Morning routine tutorial",
    product: "LuxeGlow",
    creator: "Mia Chen",
    hook_type: "tutorial",
    creator_type: "testimonial creator",
    score: 86,
  },
];

export const mockProducts = [
  { id: 1, name: "GlowPatch", score: 91 },
  { id: 2, name: "LuxeGlow", score: 86 },
];

export const mockRecommendations = [
  { id: 1, category: "useMore", name: "Problem-solution hooks" },
  { id: 2, category: "nextTest", name: "UGC creator testimonials" },
];

export default {
  dashboardStats,
  recentPerformance,
  mockCreatives,
  mockProducts,
  mockRecommendations,
};
