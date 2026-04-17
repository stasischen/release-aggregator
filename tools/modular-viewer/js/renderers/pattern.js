/**
 * Pattern Lab Renderer Component
 */

(function () {
  function renderPatternLab(node) {
    const payload = node.payload || {};
    const locale = window.currentLocale();
    const teachingLocale = window.currentTeachingLocale();

    const lessonSupportModule = window.renderLessonSupportModule(payload.lesson_support_module);

    // Slot Banks (Legacy or supplemental)
    const slotBanks = (payload.slot_bank_panels || []).map(panel => `
      <div class="content-block">
        <div class="block-title">${window.escapeHtml(window.i18nText(panel.title_i18n, locale, window.getLabel('swappable_materials')))}</div>
        <div class="compare-pros">
          ${(panel.items_i18n || panel.items || []).map(item => `
            <div class="pro-item">
              <strong>${window.escapeHtml(item.ko || item.target || '')}</strong>
              <div class="tiny-text muted" style="margin-top:3px;">${window.escapeHtml(window.i18nText(item.explain_i18n || item, locale, ''))}</div>
            </div>
          `).join('')}
        </div>
      </div>
    `).join('');

    // Pattern Builders (Handle both singular and plural)
    let buildersHtml = '';
    const builders = payload.pattern_builder_demos || (payload.pattern_builder_demo ? [payload.pattern_builder_demo] : []);
    buildersHtml = builders.map(b => window.renderPatternBuilderBlock(b, node.id)).join('');

    return `
      <div class="pattern-lab-container animate-in">
        ${window.renderNotice(payload)}
        ${lessonSupportModule}
        ${slotBanks}
        ${buildersHtml}
      </div>
    `;
  }

  // Registry
  window.RendererRegistry.registerContent('pattern_lab', renderPatternLab);
  window.RendererRegistry.registerContent('pattern_card', renderPatternLab);

  // --- Pattern Builder Engine ---

  window.renderPatternBuilderBlock = function (builder, nodeId) {
    const locale = window.currentLocale();
    const builderId = `builder-${window.escapeJsSingle(nodeId || 'x')}-${window.escapeJsSingle(builder.builder_id || 'main')}`;
    const rawConfigJson = JSON.stringify(builder);
    const configJsonAttr = window.escapeHtml(rawConfigJson);

    const savedState = (window.getNodeInteractionState && window.getNodeInteractionState(builderId)) || {};
    const savedValues = savedState; // Flatter structure for reliability

    const initialValues = {};
    (builder.controls || []).forEach(control => {
      const savedVal = savedValues[control.control_id];
      const defaultVal = (control.options && control.options[0]) ? control.options[0].value : '';
      initialValues[control.control_id] = (savedVal !== undefined && savedVal !== null) ? savedVal : defaultVal;
    });
    const initialResolvedValues = window.resolvePatternBuilderValues(builder, initialValues);
    const initialComputed = window.computePatternBuilderOutput(builder, initialResolvedValues);

    const controlsHtml = (builder.controls || []).map(control => `
      <label class="tiny-text muted" style="display:block; margin-bottom:10px;">
        <span style="display:block; margin-bottom:4px; font-weight:700;">${window.escapeHtml(window.i18nText(control.label_i18n, teachingLocale, control.control_id))}</span>
        <select data-builder-control="${window.escapeHtml(control.control_id)}"
          onchange="window.updatePatternBuilderFromRoot('${builderId}')"
          style="width:100%; padding:8px; border-radius:8px; border:1px solid var(--line); background:#fff;">
          ${window.getAvailableControlOptions(control, initialResolvedValues).map(option => `
            <option value="${window.escapeHtml(option.value)}"${option.value === initialResolvedValues[control.control_id] ? ' selected' : ''}>
              ${window.escapeHtml(window.renderOptionLabelWithGloss(option, teachingLocale))}
            </option>
          `).join('')}
        </select>
      </label>
    `).join('');

    const presetsHtml = (builder.review_export_presets || []).map(p => `
      <div class="preset-tag" onclick="window.applyPatternBuilderPreset('${builderId}', '${window.escapeHtml(JSON.stringify(p.control_values))}')">
        ${window.escapeHtml(window.i18nText(p.meaning_i18n, locale, ''))}
      </div>
    `).join('');

    return `
      <div class="content-block">
        <div class="block-title">${window.escapeHtml(window.i18nText(builder.title_i18n, teachingLocale, window.getLabel('dynamic_patterns')))}</div>
        <div id="${builderId}" class="summary-box" data-builder-config="${configJsonAttr}" data-node-id="${window.escapeHtml(nodeId)}">
          ${window.i18nText(builder.inline_hint_i18n, teachingLocale, '') ? `<div class="muted-text" style="margin-bottom:12px;">${window.escapeHtml(window.i18nText(builder.inline_hint_i18n, teachingLocale, ''))}</div>` : ''}
          <div class="summary-grid" style="grid-template-columns:repeat(3, 1fr);">
            ${controlsHtml}
          </div>
          ${presetsHtml ? `<div class="presets-row" style="margin-top:12px; display:flex; gap:8px; flex-wrap:wrap;">
            <span class="tiny-text muted" style="width:100%;">${window.getLabel('quick_presets')}</span>
            ${presetsHtml}
          </div>` : ''}
          <div class="pattern-entry" style="margin-top:12px; border-top:1px dashed var(--line); padding-top:12px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <div class="pattern-formula" data-builder-output style="flex:1;">${window.escapeHtml(initialComputed.sentence)}</div>
              <button class="btn tiny-text" data-builder-speak data-tts-text="${window.escapeHtml(initialComputed.sentence)}" onclick="window.speakKo(this.getAttribute('data-tts-text'))" style="padding:4px 8px;">▶</button>
            </div>
            <div class="pattern-use-case" data-builder-gloss>${window.escapeHtml(initialComputed.gloss)}</div>
          </div>
          <div class="debug-state-indicator tiny-text muted" style="margin-top:8px; font-size:10px; border-top:1px solid #eee; padding-top:4px;">
            Persisted Key: ${builderId}
          </div>
        </div>
      </div>
    `;
  };

  window.applyPatternBuilderPreset = function (builderId, valuesJson) {
    const root = document.getElementById(builderId);
    if (!root) return;
    const values = JSON.parse(valuesJson);
    Object.entries(values).forEach(([key, val]) => {
      const select = root.querySelector(`select[data-builder-control="${key}"]`);
      if (select) select.value = val;
    });
    window.updatePatternBuilderFromRoot(builderId);
    if (window.showToast) window.showToast(window.getLabel('applied_preset'));
  };

  window.computePatternBuilderOutput = function (config, rawValues) {
    const locale = window.currentLocale();
    const values = { ...rawValues };
    const registerKey = values.register || 'polite';
    const selectedMap = {};

    (config.controls || []).forEach(control => {
      const match = (control.options || []).find(opt => opt.value === values[control.control_id]);
      selectedMap[control.control_id] = match || null;
    });

    // 1. Register-based template
    let sentence = (config.register_templates && config.register_templates[registerKey]) || config.template || '';

    // 2. Dynamic Token Rules (i18n-safe)
    if (config.dynamic_token_rules) {
      config.dynamic_token_rules.forEach(rule => {
        const sourceOption = selectedMap[rule.source_control_id];
        const endingType = sourceOption && sourceOption.ending_type ? sourceOption.ending_type : 'batchim';
        let replacement = '';

        if (rule.map_by_register_and_value) {
          const sourceValue = values[rule.source_control_id] || '';
          replacement = (((rule.map_by_register_and_value || {})[registerKey] || {})[sourceValue]) || '';
        } else if (rule.map_by_register_and_ending) {
          replacement = (((rule.map_by_register_and_ending || {})[registerKey] || {})[endingType]) || '';
        }

        sentence = sentence.replaceAll(`{${rule.token}}`, replacement);
      });
    }

    // 3. Basic Variable Replacement
    Object.entries(values).forEach(([key, value]) => {
      sentence = sentence.replaceAll(`{${key}}`, value);
    });

    // 4. Gloss/Translation (i18n-first)
    let gloss = '';
    const transTemplate = config.translation_templates ? config.translation_templates[registerKey] : null;
    if (transTemplate) {
      gloss = window.i18nText(transTemplate, locale, '');
      // Replace variables in gloss
      Object.entries(values).forEach(([key, value]) => {
        const match = selectedMap[key];
        const gVal = match ? window.i18nText(match.gloss_i18n || match.label_i18n, locale, value) : value;
        gloss = gloss.replaceAll(`{${key}}`, gVal);
      });
    }

    return { sentence, gloss };
  };

  // Necessary for browser event handling
  window.updatePatternBuilderFromRoot = function (builderId) {
    const root = document.getElementById(builderId);
    if (!root) return;
    const config = JSON.parse(root.getAttribute('data-builder-config'));
    const selects = root.querySelectorAll('select[data-builder-control]');
    const values = {};
    selects.forEach(s => { values[s.getAttribute('data-builder-control')] = s.value; });

    // Some controls might depend on others, re-resolve if needed
    const resolvedValues = window.resolvePatternBuilderValues ? window.resolvePatternBuilderValues(config, values) : values;
    const result = window.computePatternBuilderOutput(config, resolvedValues);

    root.querySelector('[data-builder-output]').textContent = result.sentence;
    root.querySelector('[data-builder-gloss]').textContent = result.gloss;
    const speakBtn = root.querySelector('[data-builder-speak]');
    if (speakBtn) speakBtn.setAttribute('data-tts-text', result.sentence);

    // Persist state
    try {
        if (window.setNodeInteractionState) {
            window.setNodeInteractionState(builderId, values);
            if (window.showToast) window.showToast(`${window.getLabel('saved_state')}: ${builderId.split('-').pop()}`);
        }
    } catch (e) {
        console.error('Pattern persistence error', e);
    }
  };

  window.resolvePatternBuilderValues = (config, values) => values; // Pass-through for now
  window.getAvailableControlOptions = (control) => control.options || [];
  window.renderOptionLabelWithGloss = (option, locale) => {
    const label = window.i18nText(option.label_i18n, locale, option.value);
    const gloss = window.i18nText(option.gloss_i18n, locale, '');
    return gloss ? `${label} (${gloss})` : label;
  };

})();
