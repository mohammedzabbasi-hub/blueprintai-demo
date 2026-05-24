# BluePrintAI Backend Route Inventory

This document captures the Phase 10 route inventory. It is documentation only.
Do not change active route mounting, imports, or route behavior from this file
without a separate implementation phase and full regression testing.

## Active Mounted Routes

| Method | Active path | Source file | Router prefix | Mounted in `main.py` | Conflict now? |
|---|---|---|---|---|---|
| GET | `/` | `main.py` | n/a | yes | no |
| GET | `/analytics/dashboard` | `api/routes/analytics.py` | `/analytics` | yes | no |
| GET | `/creatives` | `api/routes/creatives.py` | none, mounted at `/creatives` | yes | no |
| GET | `/creatives/{creative_id}` | `api/routes/creatives.py` | none, mounted at `/creatives` | yes | no |
| GET | `/personalized/shop-state` | `routes/personalized.py` | `/personalized` | yes | no |
| GET | `/personalized/creatives` | `routes/personalized.py` | `/personalized` | yes | no |
| POST | `/personalized/creatives` | `routes/personalized.py` | `/personalized` | yes | no |
| GET | `/personalized/creatives/{creative_id}` | `routes/personalized.py` | `/personalized` | yes | no |
| GET | `/personalized/dashboard` | `routes/personalized.py` | `/personalized` | yes | no |
| GET | `/personalized/recommendations` | `routes/personalized.py` | `/personalized` | yes | no |
| GET | `/personalized/briefs` | `routes/personalized.py` | `/personalized` | yes | no |
| GET | `/personalized/creators` | `routes/personalized.py` | `/personalized` | yes | no |
| GET | `/recommendations` | `routes/recommendations.py` | none | yes | no |
| POST | `/briefs/generate` | `api/routes/briefs.py` | none, mounted at `/briefs` | yes | no |
| POST | `/onboarding/create-account` | `routes/onboarding.py` | `/onboarding` | yes | no |
| GET | `/onboarding/me` | `api/routes/onboarding.py` | `/onboarding` | yes | no |
| POST | `/onboarding/me` | `api/routes/onboarding.py` | `/onboarding` | yes | no |
| POST | `/auth/app-login` | `routes/login.py` | `/auth` | yes | no |
| POST | `/auth/register` | `api/routes/auth.py` | none, mounted at `/auth` | yes | no |
| POST | `/auth/login` | `api/routes/auth.py` | none, mounted at `/auth` | yes | no |
| GET | `/auth/me` | `api/routes/auth.py` | none, mounted at `/auth` | yes | no |
| POST | `/data-import/csv` | `routes/data_import.py` | `/data-import` | yes | no |
| POST | `/data-import/json` | `routes/data_import.py` | `/data-import` | yes | no |
| GET | `/data-import/summary` | `routes/data_import.py` | `/data-import` | yes | no |
| DELETE | `/data-import/clear` | `routes/data_import.py` | `/data-import` | yes | no |
| GET | `/demo/shops` | `routes/demo.py` | `/demo` | yes | no |
| POST | `/video-analysis/analyze` | `routes/video_analysis.py` | `/video-analysis` | yes | no |
| POST | `/creators` | `routes/creators.py` | `/creators` | yes | no |
| GET | `/creators` | `routes/creators.py` | `/creators` | yes | no |
| GET | `/creators/compare` | `routes/creators.py` | `/creators` | yes | no |
| GET | `/creators/{creator_id}` | `routes/creators.py` | `/creators` | yes | no |
| PUT | `/creators/{creator_id}` | `routes/creators.py` | `/creators` | yes | no |
| DELETE | `/creators/{creator_id}` | `routes/creators.py` | `/creators` | yes | no |
| POST | `/activity-log` | `routes/activity_log.py` | `/activity-log` | yes | no |
| GET | `/activity-log` | `routes/activity_log.py` | `/activity-log` | yes | no |
| DELETE | `/activity-log` | `routes/activity_log.py` | `/activity-log` | yes | no |
| GET | `/engine/analyze-shop` | `api/routes/engine.py` | `/engine` | yes | no |
| GET | `/engine/recommendations` | `api/routes/engine.py` | `/engine` | yes | no |
| GET | `/engine/briefs` | `api/routes/engine.py` | `/engine` | yes | no |
| GET | `/engine/strategy-summary` | `api/routes/engine.py` | `/engine` | yes | no |
| GET | `/engine/ai-payload` | `api/routes/engine.py` | `/engine` | yes | no |
| GET | `/engine/gemini-strategy` | `api/routes/engine.py` | `/engine` | yes | no |
| POST | `/blueprint/generate` | `routes/revenue_blueprint.py` | none, mounted at `/blueprint` | yes | no |
| GET | `/blueprint/{shop_id}/latest` | `routes/revenue_blueprint.py` | none, mounted at `/blueprint` | yes | no |
| POST | `/blueprint/complete-step` | `routes/revenue_blueprint.py` | none, mounted at `/blueprint` | yes | no |

## Dormant Or Unmounted Duplicate Route Families

These files contain route definitions but are not currently mounted in `main.py`,
or duplicate an active route family with a different implementation.

| Method | Would-be path | Source file | Router prefix | Mounted? | Duplicate/conflict risk |
|---|---|---|---|---|---|
| GET | `/dashboard` | `routes/analytics.py` | none | no | Duplicate analytics family |
| GET | `/analytics/dashboard` | `api/routes/analytics.backup.py` | `/analytics` | no | Exact duplicate if mounted |
| POST | `/sync` | `routes/creatives.py` | none | no | Duplicate creatives family |
| GET | `/` | `routes/creatives.py` | none | no | Would conflict if mounted under `/creatives` |
| GET | `/{creative_id}` | `routes/creatives.py` | none | no | Would conflict if mounted under `/creatives` |
| POST | `/tiktok/analyze` | `api/routes/tiktok.py` | `/tiktok` | no | Duplicate TikTok intelligence family |
| POST | `/tiktok/compare` | `api/routes/tiktok.py` | `/tiktok` | no | Duplicate TikTok intelligence family |
| POST | `/analyze` | `routes/tiktok.py` | none | no | Duplicate TikTok logic, different path |
| POST | `/compare` | `routes/tiktok.py` | none | no | Duplicate TikTok logic, different path |
| GET | `/products` | `routes/products.py` | `/products` | no | Overlaps `api/routes/products.py`; caller-provided `shop_id` style |
| GET | `/products/{product_id}` | `routes/products.py` | `/products` | no | Product detail route is dormant |
| POST | `/products/sync/{shop_id}` | `routes/products.py` | `/products` | no | Caller-provided `shop_id` style |
| GET | `/products` | `api/routes/products.py` | `/products` | no | Overlaps `routes/products.py`; current-user style |
| GET | `/orders` | `routes/orders.py` | `/orders` | no | Overlaps `api/routes/orders.py`; caller-provided `shop_id` style |
| GET | `/orders/{order_id}` | `routes/orders.py` | `/orders` | no | Order detail route is dormant |
| POST | `/orders/sync/{shop_id}` | `routes/orders.py` | `/orders` | no | Caller-provided `shop_id` style |
| GET | `/orders` | `api/routes/orders.py` | `/orders` | no | Overlaps `routes/orders.py`; current-user style |
| POST | `/generate` | `routes/briefs.py` | none | no | Same implementation shape as active `/briefs/generate` |
| GET | `/` | `api/routes/recommendations.py` | none | no | Recommendation family overlap |
| POST | `/webhooks/tiktok` | `api/routes/webhooks.py` | `/webhooks` | no | Duplicate webhook family |
| POST | `/webhooks/tiktok` | `routes/webhooks.py` | `/webhooks` | no | Duplicate webhook family |
| POST | `/webhooks/tiktok` | `routes/webhooks copy.py` | `/webhooks` | no | Duplicate copy file |
| GET | `/me` | `api/routes/settings.py` | none | no | Unsafe if mounted at root; should mount under `/settings` if revived |
| PUT | `/me` | `api/routes/settings.py` | none | no | Unsafe if mounted at root; should mount under `/settings` if revived |
| GET | `/` | `api/routes/shops.py` | none | no | Unsafe if mounted at root; should mount under `/shops` if revived |
| POST | `/connect` | `api/routes/shops.py` | none | no | Unsafe if mounted at root; should mount under `/shops` if revived |

## Recommended Implementations To Keep

- Keep `api/routes/analytics.py` for `/analytics/dashboard`.
  It is the active secured dashboard endpoint and should remain the source of
  truth for dashboard analytics.
- Keep `api/routes/creatives.py` for demo/public creative library endpoints
  mounted under `/creatives`.
- Keep `routes/personalized.py` for personalized account-specific creative,
  dashboard, recommendation, brief, and creator endpoints under `/personalized`.
- Keep `routes/onboarding.py` for `/onboarding/create-account`.
- Keep `api/routes/onboarding.py` for `/onboarding/me`.
- Keep `routes/login.py` for `/auth/app-login`.
- Keep `api/routes/auth.py` for `/auth/register`, `/auth/login`, and `/auth/me`.
- Keep `routes/data_import.py` for temporary MVP data import endpoints.
- Keep `api/routes/briefs.py` for active `/briefs/generate` unless a later
  phase replaces the hardcoded `shop_id` behavior.
- Keep `routes/recommendations.py` for the currently mounted `/recommendations`
  endpoint until recommendations are consolidated.

## Routes And Files To Deprecate Later

Do not delete these during Phase 10 documentation. They should be cleaned up only
in a later implementation phase after tests confirm no frontend, integration, or
deployment dependency still imports or calls them.

- `api/routes/analytics.backup.py`
- `routes/analytics.py`
- `routes/creatives.py`
- `routes/tiktok.py`
- `api/routes/tiktok.py` if TikTok intelligence routes are not revived
- `routes/products.py` or `api/routes/products.py`, after choosing one product API
- `routes/orders.py` or `api/routes/orders.py`, after choosing one order API
- `routes/briefs.py`
- `api/routes/recommendations.py`
- `routes/webhooks.py`, `api/routes/webhooks.py`, and `routes/webhooks copy.py`,
  after choosing one webhook implementation
- `api/routes/settings.py`, unless remounted under `/settings`
- `api/routes/shops.py`, unless remounted under `/shops`

## Regression Testing Warning

No active route changes should be made until after full regression testing.
Route consolidation can break frontend calls, auth expectations, deployment
health checks, demo account behavior, and TikTok Shop App Store review flows.
Before deleting, moving, or remounting routes, run backend route tests, frontend
build checks, browser smoke tests, and manual checks for demo and real onboarding
accounts.
