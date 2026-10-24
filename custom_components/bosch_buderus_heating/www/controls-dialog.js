// A native form selector. Draft edits never invoke an appliance service.
class BoschBuderusControls extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._changes = {};
    this._rows = [];
    this._active = "";
    // HA submits its outer form on Enter. Local navigation, details and
    // discard/refresh buttons must not submit an appliance draft.
    this.shadowRoot.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && event.target.closest("button,summary")) {
        event.stopPropagation();
      }
    });
    this.shadowRoot.innerHTML = `
      <style>
        :host{display:block;color:var(--primary-text-color)}
        *{box-sizing:border-box}
        .tabs{display:flex;flex-wrap:wrap;gap:6px;border-bottom:1px solid var(--divider-color);padding-bottom:10px}
        button{font:inherit;cursor:pointer;min-height:44px;border:0;border-radius:8px;padding:8px 12px;background:transparent;color:var(--primary-color)}
        button[aria-selected="true"]{background:var(--primary-color);color:var(--text-primary-color,#fff)}
        button:disabled,input:disabled,select:disabled{opacity:.5;cursor:default}
        button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:2px solid var(--primary-color);outline-offset:2px}
        .field{display:grid;grid-template-columns:minmax(0,1fr) minmax(110px,.8fr);gap:12px;align-items:center;padding:12px 0}
        .field label{overflow-wrap:anywhere}
        .input{display:flex;align-items:center;gap:7px;min-width:0}
        input,select{font:inherit;font-size:16px;width:100%;min-width:0;min-height:48px;padding:10px;border:0;border-bottom:1px solid var(--secondary-text-color);border-radius:4px 4px 0 0;background:var(--input-fill-color,#f1f1f1);color:var(--primary-text-color);color-scheme:var(--ha-color-scheme,light)}
        input[type="checkbox"]{width:24px;min-height:24px;height:24px;margin:10px 0;accent-color:var(--primary-color)}
        .input:has(input[type="checkbox"]){justify-content:flex-end}
        .unit{color:var(--secondary-text-color);white-space:nowrap}
        summary{cursor:pointer;padding:14px 0;color:var(--primary-color);min-height:44px}
        .actions{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:4px;margin-top:16px}
        .status{color:var(--secondary-text-color);margin:12px 0;line-height:1.5}
        .error{color:var(--error-color)}
        [hidden]{display:none}
        @media(max-width:360px){.field{grid-template-columns:minmax(0,1fr) minmax(96px,.65fr);gap:8px}}
      </style>
      <div class="tabs" role="tablist"></div>
      <div class="panels"></div>
      <p class="status" role="status" aria-live="polite"></p>
      <p class="error" role="alert"></p>
      <div class="actions"><button type="button" class="discard"></button><button type="button" class="refresh"></button></div>`;
    this.shadowRoot.querySelector(".discard").addEventListener("click", () => {
      this._changes = {};
      this._emit();
      this._render();
    });
    this.shadowRoot
      .querySelector(".refresh")
      .addEventListener("click", () => this._refresh());
  }
  get _de() {
    return (this._hass?.language || "en").startsWith("de");
  }
  _text(de, en) {
    return this._de ? de : en;
  }
  _label(labels) {
    return labels?.[this._de ? "de" : "en"] || "";
  }
  set hass(value) {
    const before = this._hass?.language;
    this._hass = value;
    if (before !== value?.language) this._render();
  }
  set selector(value) {
    const config = value?.["bosch-buderus-controls"] || {};
    if (JSON.stringify(config) === JSON.stringify(this._config)) return;
    this._config = config;
    this._rows = config.rows || [];
    this._render();
  }
  set value(value) {
    const changes = value?.changes || {};
    if (JSON.stringify(changes) === JSON.stringify(this._changes)) return;
    this._changes = { ...changes };
    this._render();
  }
  get value() {
    return { changes: { ...this._changes } };
  }
  set disabled(value) {
    this._disabled = Boolean(value);
    this._setDisabled();
  }
  set required(_value) {}
  set label(_value) {}
  focus() {
    this.shadowRoot.querySelector("button")?.focus();
  }
  reportValidity() {
    for (const input of this.shadowRoot.querySelectorAll("input,select")) {
      if (!input.disabled && !input.checkValidity()) {
        const panel = input.closest('[role="tabpanel"]');
        this._selectTab(panel.dataset.group);
        const details = input.closest("details");
        if (details) details.open = true;
        return input.reportValidity();
      }
    }
    return true;
  }
  _emit() {
    this.dispatchEvent(
      new CustomEvent("value-changed", {
        detail: { value: this.value },
        bubbles: true,
        composed: true,
      }),
    );
    this._updateStatus();
  }
  _group(group) {
    if (group === "system") return this._text("Anlage", "System");
    const [family, id] = group.split("/");
    const number = id.match(/\d+$/)?.[0] || id;
    return (
      (family === "heatingCircuits"
        ? this._text("Heizkreis ", "Heating circuit ")
        : this._text("Warmwasser ", "Hot water ")) + number
    );
  }
  _selectTab(group, focus = false) {
    this._active = group;
    for (const tab of this.shadowRoot.querySelectorAll('[role="tab"]')) {
      const active = tab.dataset.group === group;
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      if (active && focus) tab.focus();
    }
    for (const panel of this.shadowRoot.querySelectorAll('[role="tabpanel"]'))
      panel.hidden = panel.dataset.group !== group;
  }
  _render() {
    if (!this.shadowRoot) return;
    const tabs = this.shadowRoot.querySelector(".tabs");
    const panels = this.shadowRoot.querySelector(".panels");
    tabs.replaceChildren();
    panels.replaceChildren();
    tabs.setAttribute(
      "aria-label",
      this._text("Anlagenbereiche", "Appliance sections"),
    );
    const groups = [...new Set(this._rows.map((row) => row.group))];
    if (!groups.includes(this._active)) this._active = groups[0] || "";
    groups.forEach((group, index) => {
      const tab = document.createElement("button");
      tab.type = "button";
      tab.role = "tab";
      tab.id = "tab-" + index;
      tab.dataset.group = group;
      tab.textContent = this._group(group);
      tab.setAttribute("aria-controls", "panel-" + index);
      tab.addEventListener("click", () => this._selectTab(group));
      tab.addEventListener("keydown", (event) => {
        let target;
        if (event.key === "ArrowRight") target = (index + 1) % groups.length;
        if (event.key === "ArrowLeft")
          target = (index - 1 + groups.length) % groups.length;
        if (event.key === "Home") target = 0;
        if (event.key === "End") target = groups.length - 1;
        if (target !== undefined) {
          event.preventDefault();
          this._selectTab(groups[target], true);
        }
      });
      tabs.append(tab);
      const panel = document.createElement("div");
      panel.role = "tabpanel";
      panel.id = "panel-" + index;
      panel.dataset.group = group;
      panel.setAttribute("aria-labelledby", tab.id);
      const details = document.createElement("details");
      const summary = document.createElement("summary");
      summary.textContent = this._text(
        "Weitere Einstellungen",
        "More settings",
      );
      details.append(summary);
      this._rows
        .filter((row) => row.group === group)
        .forEach((row, rowIndex) => {
          const field = document.createElement("div");
          field.className = "field";
          const label = document.createElement("label");
          const id = "control-" + index + "-" + rowIndex;
          label.htmlFor = id;
          label.textContent = this._label(row.label);
          const box = document.createElement("div");
          box.className = "input";
          const input = document.createElement(
            row.kind === "select" ? "select" : "input",
          );
          input.id = id;
          input.dataset.key = row.key;
          input.dataset.available = String(row.available);
          const value = Object.hasOwn(this._changes, row.key)
            ? this._changes[row.key]
            : row.value;
          if (row.kind === "number") {
            input.type = "number";
            input.min = row.minimum;
            input.max = row.maximum;
            // Step is an editing aid. The gateway's bounds are the write contract.
            input.step = "any";
            input.inputMode = "decimal";
            input.required = true;
            input.value = value;
            const unit = document.createElement("span");
            unit.className = "unit";
            unit.textContent = row.unit;
            box.append(input, unit);
          } else if (row.kind === "switch") {
            input.type = "checkbox";
            input.role = "switch";
            input.checked = ["on", "start"].includes(value);
            box.append(input);
          } else {
            for (const choice of row.options) {
              const option = document.createElement("option");
              option.value = choice.value;
              option.textContent = this._label(choice.label);
              input.append(option);
            }
            input.value = value;
            box.append(input);
          }
          input.addEventListener("input", () => {
            const selected =
              row.kind === "switch"
                ? input.checked
                  ? row.options.some((option) => option.value === "start")
                    ? "start"
                    : "on"
                  : row.options.some((option) => option.value === "stop")
                    ? "stop"
                    : "off"
                : row.kind === "number"
                  ? input.value === ""
                    ? null
                    : Number(input.value)
                  : input.value;
            if (selected === row.value) delete this._changes[row.key];
            else this._changes[row.key] = selected;
            this._emit();
          });
          field.append(label, box);
          (row.advanced ? details : panel).append(field);
        });
      if (details.children.length > 1) panel.append(details);
      panels.append(panel);
    });
    this._selectTab(this._active);
    this.shadowRoot.querySelector(".discard").textContent = this._text(
      "Verwerfen",
      "Discard",
    );
    this.shadowRoot.querySelector(".refresh").textContent = this._text(
      "Werte neu laden",
      "Reload values",
    );
    this._updateStatus();
    this._setDisabled();
  }
  _updateStatus() {
    const count = Object.keys(this._changes).length;
    this.shadowRoot.querySelector(".status").textContent = count
      ? this._text(
          count + " ungespeicherte Änderungen",
          count + " unsaved changes",
        )
      : this._config?.status === "saved"
        ? this._text("Änderungen bestätigt.", "Changes confirmed.")
        : this._config?.status === "empty"
          ? this._text(
              "Zurzeit sind keine bedienbaren Einstellungen verfügbar.",
              "No controls are currently available.",
            )
          : this._text(
              "Änderungen werden erst mit Übernehmen geschrieben.",
              "Changes are written only when you select Apply.",
            );
  }
  _setDisabled() {
    for (const element of this.shadowRoot.querySelectorAll(
      "input,select,button",
    ))
      element.disabled =
        this._disabled || this._busy || element.dataset.available === "false";
  }
  async _refresh() {
    if (this._busy || this._disabled) return;
    let flow;
    for (
      let node = this;
      node;
      node = node.parentElement || node.getRootNode()?.host
    ) {
      if (node.localName === "step-flow-form") {
        flow = node;
        break;
      }
    }
    const error = this.shadowRoot.querySelector(".error");
    if (
      flow?.domain !== "bosch_buderus_heating" ||
      flow.step?.step_id !== "operate" ||
      !flow.flowConfig?.handleFlowStep
    ) {
      error.textContent = this._text(
        "Bitte schließe den Dialog und öffne ihn erneut.",
        "Please close and reopen the dialog.",
      );
      return;
    }
    this._busy = true;
    this._setDisabled();
    const fire = (name, detail) =>
      this.dispatchEvent(
        new CustomEvent(name, { detail, bubbles: true, composed: true }),
      );
    fire("flow-step-footer-state-changed", { loading: true });
    try {
      const step = await flow.flowConfig.handleFlowStep(
        flow.hass,
        flow.step.flow_id,
        { controls: { action: "refresh" } },
      );
      if (this.isConnected) {
        this._changes = {};
        fire("flow-update", { step });
      }
    } catch {
      error.textContent = this._text(
        "Die Werte konnten nicht neu geladen werden.",
        "The values could not be reloaded.",
      );
    } finally {
      this._busy = false;
      this._setDisabled();
      if (this.isConnected)
        fire("flow-step-footer-state-changed", { loading: false });
    }
  }
}
if (!customElements.get("ha-selector-bosch-buderus-controls")) {
  customElements.define(
    "ha-selector-bosch-buderus-controls",
    BoschBuderusControls,
  );
}
