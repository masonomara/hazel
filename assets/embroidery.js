(function () {
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

    var addLabel = openBtn.textContent.trim();
    var editLabel = openBtn.getAttribute("data-label-edit") || addLabel;
    var lastFocus = null;

    function updateCount() {
      countEl.textContent = String((input.value || "").length);
    }

    function openModal(trigger) {
      lastFocus = trigger || null;
      input.value = field.value || "";
      updateCount();
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

    function applyValue(value) {
      var clean = (value || "").trim().slice(0, maxLen);
      if (clean) {
        field.value = clean;
        field.disabled = false;
        textEl.textContent = clean;
        summary.hidden = false;
        openBtn.textContent = editLabel;
        selectOptionValue(optionControl, yesValue);
      } else {
        field.value = "";
        field.disabled = true;
        summary.hidden = true;
        openBtn.textContent = addLabel;
        selectOptionValue(optionControl, noValue);
      }
    }

    openBtn.addEventListener("click", function () {
      openModal(openBtn);
    });

    input.addEventListener("input", updateCount);

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
