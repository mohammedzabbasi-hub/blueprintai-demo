# Backup / Copy File Cleanup Report

## Summary

This report documents backup, copy, dormant, and duplicate-looking files found during the audit. No active files should be deleted before full regression testing.

## Safe Cleanup Recommendation

Do not delete backup/copy files before merging the audit-fixes-phase-1 branch. Merge the security and MVP readiness fixes first, then create a separate cleanup-backups branch.

## Backup / Copy Files Found

- BLUEPRINTAIBACKEND/routes/webhooks copy.py
- BLUEPRINTAIBACKEND/api/routes/analytics.backup.py
- BLUEPRINTAIFRONTEND/src/pages/CreativeLibrary.backup.jsx
- BLUEPRINTAIFRONTEND/src/pages/Creators.jsx.backup
- BLUEPRINTAIFRONTEND/src/pages/Onboarding.jsx.backup
- BLUEPRINTAIFRONTEND/src/pages/Index.backup.jsx
- BLUEPRINTAIFRONTEND/src/pages/Settings.backup.jsx
- BLUEPRINTAIFRONTEND/src/pages/Recommendations.backup.jsx

## Inactive Duplicate-Looking Frontend Files

- BLUEPRINTAIFRONTEND/src/pages/Dashboard.jsx
- BLUEPRINTAIFRONTEND/src/pages/UploadPage.jsx
- BLUEPRINTAIFRONTEND/src/pages/SettingsPage.jsx

## Dormant Backend Duplicate Route Families

- BLUEPRINTAIBACKEND/routes/analytics.py
- BLUEPRINTAIBACKEND/routes/creatives.py
- BLUEPRINTAIBACKEND/routes/tiktok.py
- BLUEPRINTAIBACKEND/api/routes/tiktok.py
- BLUEPRINTAIBACKEND/routes/products.py
- BLUEPRINTAIBACKEND/api/routes/products.py
- BLUEPRINTAIBACKEND/routes/orders.py
- BLUEPRINTAIBACKEND/api/routes/orders.py
- BLUEPRINTAIBACKEND/routes/briefs.py
- BLUEPRINTAIBACKEND/api/routes/recommendations.py
- BLUEPRINTAIBACKEND/routes/webhooks.py
- BLUEPRINTAIBACKEND/api/routes/webhooks.py
- BLUEPRINTAIBACKEND/api/routes/settings.py
- BLUEPRINTAIBACKEND/api/routes/shops.py

## Do Not Delete Yet

Do not delete active mounted routes or active frontend pages. Keep:
- api/routes/analytics.py
- api/routes/creatives.py
- routes/personalized.py
- routes/recommendations.py
- api/routes/briefs.py
- routes/onboarding.py
- api/routes/onboarding.py
- src/pages/Index.jsx
- src/pages/Settings.jsx
- src/pages/VideoAnalysis.jsx
- src/pages/CreativeLibrary.jsx
- src/pages/Creators.jsx
- src/pages/Recommendations.jsx
- src/pages/Onboarding.jsx

## Recommended Cleanup Order Later

1. Delete generated __pycache__ files.
2. Remove obvious frontend .backup files.
3. Remove obvious backend backup/copy files.
4. Archive inactive frontend duplicate pages.
5. Clean backend dormant duplicate route families in a separate backend cleanup branch.
6. Handle webhook cleanup only after webhook validation/idempotency is implemented and tested.
7. Run full regression testing after each cleanup batch.
