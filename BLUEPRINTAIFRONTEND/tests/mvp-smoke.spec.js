import { test, expect } from "@playwright/test";

const BASE = "http://127.0.0.1:5173";

const protectedPages = [
  "/dashboard",
  "/creative-library",
  "/recommendations",
  "/ad-briefs",
  "/revenue-blueprint",
  "/creators",
  "/data-import",
  "/upload",
  "/settings",
];

test.describe("BluePrintAI MVP authenticated smoke test", () => {
  test("login works and main MVP pages load after refresh", async ({ page }) => {
    const failures = [];

    page.on("console", (msg) => {
      if (msg.type() === "error") {
        console.log("BROWSER ERROR:", msg.text());
      }
    });

    page.on("response", (res) => {
      if (res.status() === 404) {
        console.log("NOT FOUND:", res.status(), res.url());
      }
      if (res.status() >= 500) {
        console.log("SERVER ERROR:", res.status(), res.url());
      }
    });

    await page.goto(`${BASE}/login`, { waitUntil: "domcontentloaded" });

    await page.fill('input[placeholder="you@example.com"]', "beauty@demo.com");
    await page.fill('input[placeholder="Password"]', "demo123");
    await page.click('button:has-text("Sign In")');

    await page.waitForURL("**/dashboard", { timeout: 15000 });

    for (const route of protectedPages) {
      try {
        await page.goto(`${BASE}${route}`, { waitUntil: "domcontentloaded", timeout: 15000 });
        await page.waitForTimeout(1000);

        const bodyText = await page.locator("body").innerText({ timeout: 5000 });

        if (!bodyText || bodyText.trim().length < 20) {
          failures.push(`${route}: page body looks empty`);
        }

        if (bodyText.includes("AdManagerYT")) {
          failures.push(`${route}: wrong app branding appears`);
        }

        if (bodyText.includes("404")) {
          failures.push(`${route}: shows 404`);
        }

        if (bodyText.includes("Not authenticated")) {
          failures.push(`${route}: authentication failed`);
        }

        await page.reload({ waitUntil: "domcontentloaded", timeout: 15000 });
        await page.waitForTimeout(800);

        const refreshedText = await page.locator("body").innerText({ timeout: 5000 });

        if (!refreshedText || refreshedText.trim().length < 20) {
          failures.push(`${route}: refresh produced empty page`);
        }
      } catch (err) {
        failures.push(`${route}: ${err.message}`);
      }
    }

    expect(failures, failures.join("\n")).toEqual([]);
  });
});
