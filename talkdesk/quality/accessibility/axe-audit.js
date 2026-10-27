const AxeBuilder = require('@axe-core/playwright').default;
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();

  const context = await browser.newContext();

  const page = await context.newPage();

  await page.goto('http://127.0.0.1:8001/health');

  const results = await new AxeBuilder({ page }).analyze();

  console.log(
    JSON.stringify(
      {
        violations: results.violations.length,
        passes: results.passes.length,
      },
      null,
      2
    )
  );

  await browser.close();
})();
