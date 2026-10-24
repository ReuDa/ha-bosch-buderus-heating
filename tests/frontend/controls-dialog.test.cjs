const { chromium } = require("playwright");
const path = require("node:path");
const assert = require("node:assert/strict");
(async () => {
  const browser = await chromium.launch({
    headless: true,
    channel: process.env.PLAYWRIGHT_CHANNEL || undefined,
  });
  const page = await browser.newPage({
    viewport: { width: 760, height: 1000 },
    locale: "de-DE",
  });
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.setContent(
    "<style>body{font:16px Arial;background:#f5f5f5;margin:0;padding:16px}step-flow-form{display:block;padding:24px;max-width:560px;margin:auto;background:white;border-radius:16px;--primary-color:#087eac;--primary-text-color:#222;--secondary-text-color:#666;--divider-color:#ddd;--input-fill-color:#f1f1f1;--error-color:#b00020}h1{font-size:24px;font-weight:500;margin:0 0 24px}</style><step-flow-form><h1>Anlage bedienen</h1><ha-selector-bosch-buderus-controls></ha-selector-bosch-buderus-controls></step-flow-form>",
  );
  await page.addScriptTag({
    path: path.join(
      __dirname,
      "../../custom_components/bosch_buderus_heating/www/controls-dialog.js",
    ),
  });
  await page.evaluate(() => {
    const selector = document.querySelector(
      "ha-selector-bosch-buderus-controls",
    );
    const rows = [
      {
        key: "mode",
        group: "heatingCircuits/hc1",
        kind: "select",
        label: { de: "Betriebsart", en: "Operating mode" },
        value: "manual",
        options: [
          { value: "manual", label: { de: "Manuell", en: "Manual" } },
          { value: "auto", label: { de: "Automatisch", en: "Automatic" } },
        ],
        available: true,
      },
      {
        key: "target",
        group: "heatingCircuits/hc1",
        kind: "number",
        label: { de: "Manueller Sollwert", en: "Manual setpoint" },
        value: 19,
        minimum: 5,
        maximum: 30,
        unit: "°C",
        available: true,
      },
      {
        key: "flow",
        group: "heatingCircuits/hc1",
        kind: "number",
        label: { de: "Vorlaufgrenze", en: "Flow limit" },
        value: 38,
        minimum: 25,
        maximum: 60,
        unit: "°C",
        available: true,
        advanced: true,
      },
      {
        key: "water",
        group: "dhwCircuits/dhw1",
        kind: "switch",
        label: { de: "Extra-Warmwasser", en: "Extra hot water" },
        value: "stop",
        options: [{ value: "start" }, { value: "stop" }],
        available: true,
      },
      {
        key: "away",
        group: "system",
        kind: "switch",
        label: { de: "Abwesenheit", en: "Away" },
        value: "off",
        options: [{ value: "on" }, { value: "off" }],
        available: true,
      },
    ];
    selector.hass = { language: "de" };
    selector.selector = { "bosch-buderus-controls": { rows } };
    selector.value = { changes: {} };
    window.draft = {};
    window.calls = [];
    selector.addEventListener(
      "value-changed",
      (event) => (window.draft = event.detail.value),
    );
    const form = document.querySelector("step-flow-form");
    form.domain = "bosch_buderus_heating";
    window.outerSubmits = 0;
    form.addEventListener("keydown", (event) => {
      if (event.key === "Enter") window.outerSubmits++;
    });
    form.step = { step_id: "operate", flow_id: "example" };
    form.hass = {};
    form.flowConfig = {
      handleFlowStep: async (_hass, _id, data) => {
        window.calls.push(data);
        return { step_id: "operate" };
      },
    };
  });
  const ui = page.locator("ha-selector-bosch-buderus-controls");
  await ui.getByLabel("Manueller Sollwert", { exact: true }).fill("20.5");
  assert.deepEqual(await page.evaluate(() => window.draft), {
    changes: { target: 20.5 },
  });
  await ui
    .getByRole("tab", { name: "Warmwasser 1", exact: true })
    .press("Enter");
  assert.equal(await page.evaluate(() => window.outerSubmits), 0);
  await ui.getByRole("tab", { name: "Warmwasser 1", exact: true }).click();
  await ui.getByLabel("Extra-Warmwasser", { exact: true }).check();
  assert.deepEqual(await page.evaluate(() => window.draft), {
    changes: { target: 20.5, water: "start" },
  });
  assert.equal(await page.evaluate(() => window.calls.length), 0);
  await ui.getByRole("tab", { name: "Heizkreis 1", exact: true }).click();
  assert.equal(
    await ui.getByLabel("Manueller Sollwert", { exact: true }).inputValue(),
    "20.5",
  );
  await ui
    .getByRole("button", { name: "Verwerfen", exact: true })
    .press("Enter");
  assert.equal(await page.evaluate(() => window.outerSubmits), 0);
  assert.equal(
    await ui.getByLabel("Manueller Sollwert", { exact: true }).inputValue(),
    "19",
  );
  await ui.locator("summary").click();
  await ui.getByLabel("Vorlaufgrenze", { exact: true }).fill("999");
  assert.equal(await ui.evaluate((el) => el.reportValidity()), false);
  await ui.getByRole("button", { name: "Verwerfen", exact: true }).click();
  for (const width of [320, 390, 736]) {
    await page.setViewportSize({ width, height: 1000 });
    const size = await ui.evaluate((el) => ({
      client: el.clientWidth,
      scroll: el.scrollWidth,
    }));
    assert.ok(size.scroll <= size.client + 1, JSON.stringify(size));
  }
  await page.setViewportSize({ width: 390, height: 1000 });
  await ui
    .getByRole("button", { name: "Werte neu laden", exact: true })
    .click();
  assert.deepEqual(await page.evaluate(() => window.calls), [
    { controls: { action: "refresh" } },
  ]);
  await ui.evaluate((el) => {
    el.hass = { language: "en" };
  });
  assert.equal(
    await ui.getByLabel("Manual setpoint", { exact: true }).inputValue(),
    "19",
  );
  await ui
    .getByRole("tab", { name: "Heating circuit 1", exact: true })
    .press("ArrowRight");
  assert.equal(
    await ui
      .getByRole("tab", { name: "Hot water 1", exact: true })
      .getAttribute("aria-selected"),
    "true",
  );
  await ui.evaluate((el) => {
    el.disabled = true;
  });
  assert.equal(
    await ui.getByLabel("Extra hot water", { exact: true }).isDisabled(),
    true,
  );
  assert.deepEqual(errors, []);
  console.log(
    "Actual controls module: drafts, tabs, discard, validation, refresh, DE/EN, keyboard, disabled controls and 320/390/736px layout passed.",
  );
  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
