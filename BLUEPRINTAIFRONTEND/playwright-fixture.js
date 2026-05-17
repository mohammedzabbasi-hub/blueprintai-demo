import { test as base, expect } from "@playwright/test";

export const test = base.extend({
    appUrl: async ({}, use) => {
        await use("http://127.0.0.1:5173");
    }
});

export { expect };