(function () {
  // Fixed embroidery thread colors. The preview text uses the hex for the
  // selected thread color.
  var THREAD_COLORS = {
    White: "#EFEFEF",
    "Light Pink": "#FFADCE",
    Navy: "#1B3173",
    "Light Blue": "#ACC4F1",
    Black: "#1A1A1A",
  };
  var DEFAULT_TEXT_COLOR = "#1A1A1A";

  // Matching is tolerant of casing and stray/non-breaking whitespace so a
  // product option value like "Navy blue" or "Pink " still resolves.
  function normalizeColorName(name) {
    return String(name || "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim();
  }

  var THREAD_COLORS_NORMALIZED = {};
  for (var threadKey in THREAD_COLORS) {
    if (Object.prototype.hasOwnProperty.call(THREAD_COLORS, threadKey)) {
      THREAD_COLORS_NORMALIZED[normalizeColorName(threadKey)] = THREAD_COLORS[threadKey];
    }
  }

  function threadColorFor(name) {
    return THREAD_COLORS_NORMALIZED[normalizeColorName(name)] || DEFAULT_TEXT_COLOR;
  }

  function findOptionControl(variantSelects, optionName) {
    if (!variantSelects || !optionName) return null;
    var select = variantSelects.querySelector('select[name="options[' + optionName + ']"]');
    if (select) return { type: "select", select: select };
    var radios = variantSelects.querySelectorAll('input[type="radio"][name="' + optionName + '"]');
    if (radios.length) return { type: "radio", radios: radios };
    return null;
  }

  function hideOptionControl(control) {
    var node = control.type === "select" ? control.select : control.radios[0];
    var block = node.closest(".product-form__input");
    if (block) block.style.display = "none";
  }

  function selectOptionValue(control, value) {
    if (!control || !value) return;
    if (control.type === "select") {
      var hasOption = false;
      for (var i = 0; i < control.select.options.length; i++) {
        if (control.select.options[i].value === value) {
          hasOption = true;
          break;
        }
      }
      if (!hasOption) return;
      if (control.select.value === value) return;
      control.select.value = value;
      control.select.dispatchEvent(new Event("change", { bubbles: true }));
      return;
    }
    for (var j = 0; j < control.radios.length; j++) {
      var radio = control.radios[j];
      if (radio.value === value) {
        if (!radio.checked) {
          radio.checked = true;
          radio.dispatchEvent(new Event("change", { bubbles: true }));
        }
        return;
      }
    }
  }

  function optionValues(control) {
    var values = [];
    if (!control) return values;
    if (control.type === "select") {
      for (var i = 0; i < control.select.options.length; i++) {
        values.push(control.select.options[i].value);
      }
    } else {
      for (var j = 0; j < control.radios.length; j++) {
        values.push(control.radios[j].value);
      }
    }
    return values;
  }

  function currentOptionValue(control) {
    if (!control) return "";
    if (control.type === "select") return control.select.value;
    for (var i = 0; i < control.radios.length; i++) {
      if (control.radios[i].checked) return control.radios[i].value;
    }
    return "";
  }

  // Resolve `wanted` to the actual option value string on the control, matching
  // tolerantly (case + whitespace) so a small config mismatch still flips.
  function matchOptionValue(control, wanted) {
    if (!control || !wanted) return null;
    var target = normalizeColorName(wanted);
    var values = optionValues(control);
    for (var i = 0; i < values.length; i++) {
      if (normalizeColorName(values[i]) === target) return values[i];
    }
    return null;
  }

  function populateSelect(select, values) {
    for (var i = 0; i < values.length; i++) {
      var option = document.createElement("option");
      option.value = values[i];
      option.textContent = values[i];
      select.appendChild(option);
    }
  }

  // Parse the product.variants JSON that Dawn embeds inside <variant-selects>.
  function getVariantData(variantSelects) {
    if (!variantSelects) return null;
    var script = variantSelects.querySelector('script[type="application/json"]');
    if (!script) return null;
    try {
      var data = JSON.parse(script.textContent);
      return Array.isArray(data) ? data : null;
    } catch (e) {
      return null;
    }
  }

  // Option names in product order, so they line up with variant.options[i].
  function getOrderedOptionNames(variantSelects) {
    var names = [];
    var seen = {};
    var controls = variantSelects.querySelectorAll(
      'select[name^="options["], input[type="radio"][name]'
    );
    for (var i = 0; i < controls.length; i++) {
      var el = controls[i];
      var name = null;
      if (el.tagName === "SELECT") {
        var m = el.getAttribute("name").match(/^options\[(.*)\]$/);
        name = m ? m[1] : null;
      } else {
        name = el.getAttribute("name");
      }
      if (name && !seen[name]) {
        seen[name] = true;
        names.push(name);
      }
    }
    return names;
  }

  // Pick the best variant: every `hard` constraint must match; among those,
  // prefer in-stock and the most `prefer` matches. Matching is normalized.
  function chooseVariant(variants, optionNames, hard, prefer) {
    var best = null;
    var bestScore = -1;
    for (var vi = 0; vi < variants.length; vi++) {
      var v = variants[vi];
      if (!v || !v.options) continue;
      var ok = true;
      for (var hn in hard) {
        if (!hard.hasOwnProperty(hn)) continue;
        var hidx = optionNames.indexOf(hn);
        if (hidx === -1) continue;
        if (normalizeColorName(v.options[hidx]) !== normalizeColorName(hard[hn])) {
          ok = false;
          break;
        }
      }
      if (!ok) continue;
      var score = v.available ? 1000 : 0;
      for (var pn in prefer) {
        if (!prefer.hasOwnProperty(pn)) continue;
        var pidx = optionNames.indexOf(pn);
        if (pidx === -1 || prefer[pn] == null) continue;
        if (normalizeColorName(v.options[pidx]) === normalizeColorName(prefer[pn])) {
          score += 1;
        }
      }
      if (score > bestScore) {
        bestScore = score;
        best = v;
      }
    }
    return best;
  }

  function applyVariant(variant, variantSelects, optionNames) {
    if (!variant || !variant.options) return;
    for (var i = 0; i < optionNames.length; i++) {
      var control = findOptionControl(variantSelects, optionNames[i]);
      if (control) selectOptionValue(control, variant.options[i]);
    }
  }

  function initRoot(root) {
    if (root.dataset.embroideryInit === "true") return;
    root.dataset.embroideryInit = "true";

    var field = root.querySelector("[data-embroidery-field]");
    var openBtn = root.querySelector("[data-embroidery-open]");
    var modal = root.querySelector("[data-embroidery-modal]");
    var input = root.querySelector("[data-embroidery-input]");
    var saveBtn = root.querySelector("[data-embroidery-save]");
    var removeBtn = root.querySelector("[data-embroidery-remove]");
    var summary = root.querySelector("[data-embroidery-summary]");
    var textEl = root.querySelector("[data-embroidery-text]");
    var countEl = root.querySelector("[data-embroidery-count]");

    if (!field || !openBtn || !modal || !input || !saveBtn || !removeBtn) return;

    var maxLen = parseInt(root.getAttribute("data-max"), 10) || 50;
    var sectionId = root.getAttribute("data-section-id");
    var optionName = root.getAttribute("data-option-name");
    var yesValue = root.getAttribute("data-yes-value");
    var noValue = root.getAttribute("data-no-value");

    var variantSelects = sectionId ? document.getElementById("variant-selects-" + sectionId) : null;
    var optionControl = findOptionControl(variantSelects, optionName);
    if (optionControl) hideOptionControl(optionControl);

    var variantData = getVariantData(variantSelects);
    var optionNames = variantSelects ? getOrderedOptionNames(variantSelects) : [];

    var threadOptionName = root.getAttribute("data-thread-option-name");
    var threadControl = findOptionControl(variantSelects, threadOptionName);
    var threadField = root.querySelector("[data-embroidery-thread-field]");
    var threadSelect = root.querySelector("[data-embroidery-thread]");
    if (threadControl && threadField && threadSelect) {
      populateSelect(threadSelect, optionValues(threadControl));
      threadSelect.value = currentOptionValue(threadControl);
      threadField.hidden = false;
    }

    // Live preview: text follows the input, color follows the selected thread,
    // background follows the selected Color variant (hex_color) or display_color.
    var preview = root.querySelector("[data-embroidery-preview]");
    var previewText = root.querySelector("[data-embroidery-preview-text]");
    var displayColor = root.getAttribute("data-display-color") || "";
    var colorOptionName = root.getAttribute("data-color-option-name") || "Color";
    var colorControl = findOptionControl(variantSelects, colorOptionName);
    var colorMap = {};
    var colorMapEl = root.querySelector("[data-embroidery-colors]");
    if (colorMapEl) {
      try {
        colorMap = JSON.parse(colorMapEl.textContent || "{}");
      } catch (e) {
        colorMap = {};
      }
    }

    function updatePreviewText() {
      if (previewText) previewText.textContent = input.value || "";
    }

    function updatePreviewColor() {
      if (!previewText) return;
      var threadVal = threadSelect ? threadSelect.value : "";
      previewText.style.color = threadColorFor(threadVal);
    }

    function updatePreviewBackground() {
      if (!preview) return;
      var bg = "";
      if (colorControl) {
        var current = currentOptionValue(colorControl);
        if (current && colorMap[current]) bg = colorMap[current];
      }
      if (!bg && displayColor) bg = displayColor;
      // Empty string clears the inline style and falls back to the CSS default
      // (theme background color).
      preview.style.backgroundColor = bg;
    }

    if (threadSelect) threadSelect.addEventListener("change", updatePreviewColor);

    if (colorControl) {
      if (colorControl.type === "select") {
        colorControl.select.addEventListener("change", updatePreviewBackground);
      } else {
        for (var c = 0; c < colorControl.radios.length; c++) {
          colorControl.radios[c].addEventListener("change", updatePreviewBackground);
        }
      }
    }

    updatePreviewText();
    updatePreviewColor();
    updatePreviewBackground();

    var addLabel = openBtn.textContent.trim();
    var editLabel = openBtn.getAttribute("data-label-edit") || addLabel;
    var lastFocus = null;

    function updateCount() {
      countEl.textContent = String((input.value || "").length);
    }

    function openModal(trigger) {
      lastFocus = trigger || null;
      input.value = field.value || "";
      if (threadControl && threadSelect) threadSelect.value = currentOptionValue(threadControl);
      updateCount();
      updatePreviewText();
      updatePreviewColor();
      updatePreviewBackground();
      if (typeof modal.showModal === "function") {
        modal.showModal();
      } else {
        modal.setAttribute("open", "");
      }
      input.focus();
    }

    function closeModal() {
      if (typeof modal.close === "function") {
        modal.close();
      } else {
        modal.removeAttribute("open");
      }
    }

    function restoreFocus() {
      openBtn.focus();
    }

    function onOptionValue() {
      return matchOptionValue(optionControl, yesValue) || yesValue;
    }

    function offOptionValue() {
      // Prefer the configured off value; if it doesn't match a real option,
      // fall back to the first value that isn't the embroidered one.
      var off = matchOptionValue(optionControl, noValue);
      if (off) return off;
      var onValue = onOptionValue();
      var values = optionValues(optionControl);
      for (var i = 0; i < values.length; i++) {
        if (values[i] !== onValue) return values[i];
      }
      return noValue;
    }

    // Flip the embroidery option, but resolve to a variant that actually exists
    // and is in stock so toggling never lands on a sold-out combination (e.g.
    // a thread color that the standard variant doesn't offer).
    function setEmbroidery(on) {
      var targetValue = on ? onOptionValue() : offOptionValue();

      if (variantData && optionNames.length && optionName) {
        var current = {};
        for (var i = 0; i < optionNames.length; i++) {
          current[optionNames[i]] = currentOptionValue(
            findOptionControl(variantSelects, optionNames[i])
          );
        }

        // Keep every other selection (color, size, …) exactly as the customer
        // chose it — only the embroidery option and the thread may move.
        var hard = {};
        hard[optionName] = targetValue;
        for (var n in current) {
          if (!current.hasOwnProperty(n)) continue;
          if (n === optionName || n === threadOptionName) continue;
          hard[n] = current[n];
        }

        var prefer = {};
        if (on && threadOptionName && threadSelect) {
          // Honor the chosen thread; only relax it if no such variant exists.
          hard[threadOptionName] = threadSelect.value;
        } else if (threadOptionName && threadSelect) {
          // Turning off: prefer keeping the thread, but an available standard
          // variant wins over an exact thread match.
          prefer[threadOptionName] = threadSelect.value;
        }

        var variant = chooseVariant(variantData, optionNames, hard, prefer);
        if (!variant && on && threadOptionName) {
          // Chosen thread isn't available; relax it to a preference.
          delete hard[threadOptionName];
          prefer[threadOptionName] = threadSelect.value;
          variant = chooseVariant(variantData, optionNames, hard, prefer);
        }

        if (variant) {
          applyVariant(variant, variantSelects, optionNames);
          if (threadControl && threadSelect) {
            threadSelect.value = currentOptionValue(threadControl);
          }
          return;
        }
      }

      // Fallback: simple toggle when variant data isn't available.
      selectOptionValue(optionControl, targetValue);
      if (on && threadControl && threadSelect) {
        selectOptionValue(threadControl, threadSelect.value);
      }
    }

    function applyValue(value) {
      var clean = (value || "").trim().slice(0, maxLen);
      if (clean) {
        field.value = clean;
        field.disabled = false;
        textEl.textContent = clean;
        summary.hidden = false;
        openBtn.textContent = editLabel;
        setEmbroidery(true);
      } else {
        field.value = "";
        field.disabled = true;
        summary.hidden = true;
        openBtn.textContent = addLabel;
        setEmbroidery(false);
      }
    }

    openBtn.addEventListener("click", function () {
      openModal(openBtn);
    });

    input.addEventListener("input", function () {
      updateCount();
      updatePreviewText();
    });

    saveBtn.addEventListener("click", function () {
      applyValue(input.value);
      closeModal();
    });

    removeBtn.addEventListener("click", function () {
      input.value = "";
      applyValue("");
      closeModal();
    });

    modal.addEventListener("click", function (event) {
      if (event.target === modal) closeModal();
    });

    modal.addEventListener("close", restoreFocus);
  }

  function initAll() {
    var roots = document.querySelectorAll("[data-embroidery]");
    for (var i = 0; i < roots.length; i++) initRoot(roots[i]);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
