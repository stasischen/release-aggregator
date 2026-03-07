/**
 * Lingourmet Mockup Content Renderers & Registry logic
 */
if (typeof window.i18nText !== 'function') {
  window.i18nText = function (obj, locale = 'zh_tw', fallback = '') {
    if (!obj) return fallback;
    if (typeof obj === 'string') return obj;
    if (obj[locale]) return obj[locale];
    if (obj.zh_tw) return obj.zh_tw;
    if (obj.en) return obj.en;
    const first = Object.values(obj).find(v => typeof v === 'string' && v);
    return first || fallback;
  };
}

window.showBilingual = function () {
  return window.state.progress.prefs.showBilingual !== false;
};

const currentLocale = function () {
  return window.currentTeachingLocale ? window.currentTeachingLocale() : 'zh_tw';
};

window.warnUnresolvedTemplate = function (scope, template, context = {}) {
  if (!template || typeof template !== 'string') return;
  const matches = template.match(/\{[^}]+\}/g);
  if (!matches || !matches.length) return;
  console.warn(`[mockup-template-warning] ${scope} has unresolved token(s): ${matches.join(', ')}`, context);
};

window.renderOptionLabelWithGloss = function (option, locale) {
  if (!option) return '';
  const label = window.i18nText(option.label_i18n, locale, option.label_zh_tw || option.value || '');
  const gloss = window.i18nText(option.gloss_i18n, locale, option.gloss_zh_tw || '');
  if (!gloss || gloss === label) return label;
  if (label.includes(gloss)) return label;
  return `${label} · ${gloss}`;
};

window.optionMatchesAvailability = function (option, values) {
  if (!option || !option.available_when) return true;
  return Object.entries(option.available_when).every(([controlId, allowed]) => {
    const allowedValues = Array.isArray(allowed) ? allowed : [allowed];
    return allowedValues.includes(values[controlId]);
  });
};

window.getAvailableControlOptions = function (control, values) {
  const options = (control.options || []).filter(option => window.optionMatchesAvailability(option, values));
  return options.length ? options : (control.options || []);
};

window.resolvePatternBuilderValues = function (config, seedValues = {}) {
  const values = { ...seedValues };
  (config.controls || []).forEach(control => {
    const availableOptions = window.getAvailableControlOptions(control, values);
    const currentValue = values[control.control_id];
    const stillValid = availableOptions.some(option => option.value === currentValue);
    values[control.control_id] = stillValid
      ? currentValue
      : (availableOptions[0] ? availableOptions[0].value : '');
  });
  return values;
};

window.syncPatternBuilderControls = function (root, config, seedValues, locale) {
  const resolvedValues = window.resolvePatternBuilderValues(config, seedValues);
  (config.controls || []).forEach(control => {
    const select = root.querySelector(`[data-builder-control="${control.control_id}"]`);
    if (!select) return;
    const availableOptions = window.getAvailableControlOptions(control, resolvedValues);
    select.innerHTML = availableOptions.map(option => (
      `<option value="${window.escapeHtml(option.value)}">${window.escapeHtml(window.renderOptionLabelWithGloss(option, locale))}</option>`
    )).join('');
    select.value = resolvedValues[control.control_id] || '';
  });
  return resolvedValues;
};

// --- Renderer Registry Contract ---

window.RendererRegistry = {
  contentRenderers: {},     // keyed by content_form
  interactionRenderers: {}, // keyed by output_mode
  combinedRenderers: {},    // keyed by "form:mode" for special cases

  registerContent(form, fn) {
    this.contentRenderers[form] = fn;
  },

  registerInteraction(mode, fn) {
    this.interactionRenderers[mode] = fn;
  },

  registerCombined(form, mode, fn) {
    this.combinedRenderers[`${form}:${mode}`] = fn;
  },

  /**
   * Dispatch rendering for a node.
   * Returns: { contentHtml, interactionHtml }
   */
  dispatch(node) {
    const payload = node.payload || {};
    const form = node.content_form || 'unknown';
    const mode = node.output_mode || 'none';

    let contentHtml = '';
    let interactionHtml = '';

    // 1. Combined Priority
    const combinedKey = `${form}:${mode}`;
    if (this.combinedRenderers[combinedKey]) {
      // Note: Combined renderers return an object or handle both
      const result = this.combinedRenderers[combinedKey](payload, node);
      if (typeof result === 'string') {
        contentHtml = result;
      } else {
        contentHtml = result.contentHtml || '';
        interactionHtml = result.interactionHtml || '';
      }
    } else {
      // 2. Standard content dispatch
      if (this.contentRenderers[form]) {
        contentHtml = this.contentRenderers[form](payload, node);
      } else {
        contentHtml = this.renderUnknownForm(form, payload);
      }

      // 3. Standard interaction dispatch
      if (mode !== 'none' && mode !== 'unknown') {
        if (this.interactionRenderers[mode]) {
          interactionHtml = this.interactionRenderers[mode](node);
        } else {
          interactionHtml = this.renderUnsupportedMode(mode);
        }
      }
    }

    return { contentHtml, interactionHtml };
  },

  // --- Fallback Renderers ---

  renderUnknownForm(form, payload) {
    return `
            <div class="interaction-panel" style="border-color:var(--warn); background:var(--warn-soft);">
                <div class="interaction-label" style="color:var(--warn);">⚠️ 未知的內容形式 (Unknown Form)</div>
                <div class="muted-text" style="margin-bottom:12px;">
                    系統無法識別 <code>content_form: "${window.escapeHtml(form)}"</code>。
                </div>
                <details style="font-size:11px; color:var(--muted);">
                    <summary>檢視原始數據 (Payload)</summary>
                    <pre style="background:#fff; padding:8px; border-radius:4px; margin-top:4px; overflow:auto;">${window.escapeHtml(JSON.stringify(payload, null, 2))}</pre>
                </details>
            </div>
        `;
  },

  renderUnsupportedMode(mode) {
    return `
            <div class="interaction-panel" style="border-style:dashed; opacity:0.7;">
                <div class="interaction-label" style="color:var(--muted);">ℹ️ 不支援的互動模式 (Unsupported Mode)</div>
                <div class="muted-text">
                    當前 Viewer 尚未實作 <code>output_mode: "${window.escapeHtml(mode)}"</code> 的互動邏輯。
                </div>
            </div>
        `;
  },

  renderMalformedPayload(form, mode, missingFields) {
    return `
             <div class="interaction-panel" style="border-color:var(--accent); background:var(--accent-soft);">
                <div class="interaction-label">❌ 數據格式錯誤 (Malformed Payload)</div>
                <div class="muted-text">
                    <code>${form}:${mode}</code> 缺漏必要欄位: <strong>${missingFields.join(', ')}</strong>
                </div>
            </div>
        `;
  }
};

// --- Detail Rendering Helpers ---

window.renderDetailHeader = function (node) {
  const locale = window.currentTeachingLocale();
  const header = document.getElementById('detailHeader');
  header.innerHTML = `
    <div class="content-header animate-in">
      <div class="type-tags">
        <span class="type-tag">${node.learning_role}</span>
        <span class="type-tag" style="background:var(--accent2-soft); color:var(--accent2);">${node.candidate_type}</span>
      </div>
      <h1>${window.escapeHtml(window.i18nText(node.title_i18n, locale, node.title_zh_tw || ''))}</h1>
    </div>
  `;
};

window.renderDetailSummary = function (node) {
  const locale = window.currentTeachingLocale();
  const summaryText = window.i18nText(node.summary_i18n, locale, node.summary_zh_tw || '');
  const expectedText = window.i18nText(node.expected_output_i18n, locale, node.expected_output_zh_tw || '觀察與理解');
  const summaryBox = document.getElementById('detailSummary');
  summaryBox.innerHTML = `
    <div class="content-summary animate-in">
      <div style="font-weight:700; margin-bottom:8px;">本節目標</div>
      <div class="muted-text">${window.escapeHtml(summaryText)}</div>
      <div class="summary-grid">
        <div class="summary-box">
          <span class="label">預期輸出</span>
          ${window.escapeHtml(expectedText)}
        </div>
        <div class="summary-box">
          <span class="label">技能焦查</span>
          ${(node.skill_focus || []).join(' / ')}
        </div>
      </div>
    </div>
  `;
};

// --- Content Form implementation functions ---

window.updatePatternBuilder = function (builderId, configJson) {
  let config;
  try {
    config = JSON.parse(configJson);
  } catch (err) {
    return;
  }

  const root = document.getElementById(builderId);
  if (!root) return;

  const outputEl = root.querySelector('[data-builder-output]');
  const glossEl = root.querySelector('[data-builder-gloss]');
  const speakEl = root.querySelector('[data-builder-speak]');
  if (!outputEl) return;

  const seedValues = {};
  (config.controls || []).forEach(control => {
    const select = root.querySelector(`[data-builder-control="${control.control_id}"]`);
    seedValues[control.control_id] = select ? select.value : '';
  });
  const values = window.syncPatternBuilderControls(root, config, seedValues, currentLocale());

  const registerKey = values.register || 'polite';
  const computed = window.computePatternBuilderOutput(config, values);

  const speakerSelect = root.querySelector('[data-builder-control="speaker"]');
  if (speakerSelect && computed.values && computed.values.speaker) {
    speakerSelect.value = computed.values.speaker;
  }

  outputEl.textContent = computed.sentence;
  if (glossEl) glossEl.textContent = computed.gloss;
  if (speakEl) {
    if (computed.sentence && window.ttsSupported && window.ttsSupported()) {
      speakEl.style.display = '';
      speakEl.setAttribute('data-tts-text', computed.sentence);
      speakEl.setAttribute('title', '播放目前句子');
    } else {
      speakEl.style.display = 'none';
      speakEl.removeAttribute('data-tts-text');
    }
  }
};

window.updatePatternBuilderFromRoot = function (builderId) {
  const root = document.getElementById(builderId);
  if (!root) return;
  const configJson = root.getAttribute('data-builder-config');
  if (!configJson) return;
  window.updatePatternBuilder(builderId, configJson);
};

window.applyPatternBuilderPreset = function (builderId, presetJson) {
  const root = document.getElementById(builderId);
  if (!root) return;
  let preset;
  try {
    preset = JSON.parse(presetJson);
  } catch (err) {
    return;
  }

  Object.entries(preset).forEach(([controlId, value]) => {
    const select = root.querySelector(`[data-builder-control="${controlId}"]`);
    if (select) select.value = value;
  });

  window.updatePatternBuilderFromRoot(builderId);
};

window.applyPatternBuilderSlotValue = function (builderId, controlId, value) {
  const root = document.getElementById(builderId);
  if (!root) return;
  const select = root.querySelector(`[data-builder-control="${controlId}"]`);
  if (!select) return;
  select.value = value;
  window.updatePatternBuilderFromRoot(builderId);
};

window.computePatternBuilderOutput = function (config, rawValues) {
  const locale = window.currentTeachingLocale ? window.currentTeachingLocale() : 'zh_tw';
  const values = { ...rawValues };
  const registerKey = values.register || 'polite';
  const selectedMap = {};

  (config.controls || []).forEach(control => {
    const match = (control.options || []).find(opt => opt.value === values[control.control_id]);
    selectedMap[control.control_id] = match || null;
  });

  if (config.control_rules && config.control_rules.speaker_by_register) {
    const allowedSpeaker = config.control_rules.speaker_by_register[registerKey];
    if (allowedSpeaker) {
      values.speaker = allowedSpeaker;
      selectedMap.speaker = ((config.controls || []).find(c => c.control_id === 'speaker')?.options || []).find(opt => opt.value === allowedSpeaker) || selectedMap.speaker;
    }
  }

  if (config.value_derivation_rules && config.value_derivation_rules.length) {
    config.value_derivation_rules.forEach(rule => {
      const sourceOption = selectedMap[rule.from_control_id];
      let derivedValues = null;
      if (sourceOption && sourceOption.sentence_values_by_register && sourceOption.sentence_values_by_register[registerKey]) {
        derivedValues = sourceOption.sentence_values_by_register[registerKey];
      } else if (sourceOption && sourceOption.sentence_values) {
        derivedValues = sourceOption.sentence_values;
      }
      if (!derivedValues) return;
      (rule.assign || []).forEach(targetKey => {
        if (Object.prototype.hasOwnProperty.call(derivedValues, targetKey)) {
          values[targetKey] = derivedValues[targetKey];
        }
      });
    });
  }

  let sentence = (config.register_templates && config.register_templates[registerKey]) || '';

  if (config.dynamic_token_rules && config.dynamic_token_rules.length) {
    config.dynamic_token_rules.forEach(rule => {
      const sourceOption = selectedMap[rule.source_control_id];
      const endingType = sourceOption && sourceOption.ending_type ? sourceOption.ending_type : 'batchim';
      let replacement = '';

      if (rule.map_by_register_and_ending) {
        replacement = (((rule.map_by_register_and_ending || {})[registerKey] || {})[endingType]) || '';
      } else if (rule.map_by_register_and_value) {
        const sourceValue = values[rule.source_control_id] || '';
        replacement = (((rule.map_by_register_and_value || {})[registerKey] || {})[sourceValue]) || '';
      } else if (rule.map_by_ending) {
        replacement = (rule.map_by_ending || {})[endingType] || '';
      }

      sentence = sentence.replaceAll(`{${rule.token}}`, replacement);
    });
  } else if (config.dynamic_suffix_rules && values.identity) {
    const identityOption = selectedMap.identity;
    const endingType = identityOption && identityOption.ending_type ? identityOption.ending_type : 'batchim';
    const copulaMap = config.dynamic_suffix_rules.copula_by_register_and_ending || {};
    const copula = copulaMap[registerKey] && copulaMap[registerKey][endingType] ? copulaMap[registerKey][endingType] : '';
    sentence = sentence.replaceAll('{copula}', copula);
  }

  Object.entries(values).forEach(([key, value]) => {
    sentence = sentence.replaceAll(`{${key}}`, value);
  });
  window.warnUnresolvedTemplate(`sentence:${config.builder_id || 'unknown'}`, sentence, {
    values,
    registerKey,
  });

  let gloss = '';
  if (config.translation_templates && config.translation_templates[registerKey]) {
    gloss = window.i18nText(config.translation_templates[registerKey], locale, '');
    Object.entries(values).forEach(([key, value]) => {
      const match = selectedMap[key];
      const glossValue = match ? window.i18nText(match.gloss_i18n, locale, match.gloss_zh_tw || value) : value;
      gloss = gloss.replaceAll(`{${key}}`, glossValue);
    });
    Object.entries(selectedMap).forEach(([key, match]) => {
      if (!match) return;
      const glossValue = window.i18nText(match.gloss_i18n, locale, match.gloss_zh_tw || match.value || '');
      gloss = gloss.replaceAll(`{${key}}`, glossValue);
    });
    if (selectedMap.register) {
      const registerGloss = window.i18nText(selectedMap.register.gloss_i18n, locale, selectedMap.register.gloss_zh_tw || '');
      if (registerGloss) gloss = gloss.replaceAll('{register}', registerGloss);
    }
    window.warnUnresolvedTemplate(`gloss:${config.builder_id || 'unknown'}:${locale}`, gloss, {
      values,
      registerKey,
      locale,
    });
  }

  return { values, selectedMap, sentence, gloss };
};

window.renderPatternBuilderBlock = function (builder, nodeId) {
  const locale = currentLocale();
  const builderId = `builder-${window.escapeJsSingle(nodeId || builder.builder_id || 'x')}-${window.escapeJsSingle(builder.builder_id || 'main')}`;
  const rawConfigJson = JSON.stringify(builder);
  const configJsonAttr = window.escapeHtml(rawConfigJson);

  const initialValues = {};
  (builder.controls || []).forEach(control => {
    initialValues[control.control_id] = control.options && control.options[0] ? control.options[0].value : '';
  });
  const initialResolvedValues = window.resolvePatternBuilderValues(builder, initialValues);

  const controlsHtml = (builder.controls || []).map(control => `
    <label class="tiny-text muted" style="display:block; margin-bottom:10px;">
      <span style="display:block; margin-bottom:4px; font-weight:700;">${window.escapeHtml(window.i18nText(control.label_i18n, locale, control.label_zh_tw || control.control_id))}</span>
      <select data-builder-control="${window.escapeHtml(control.control_id)}"
        onchange="window.updatePatternBuilderFromRoot('${builderId}')"
        style="width:100%; padding:8px; border-radius:8px; border:1px solid var(--line); background:#fff;">
        ${window.getAvailableControlOptions(control, initialResolvedValues).map(option => `<option value="${window.escapeHtml(option.value)}"${option.value === initialResolvedValues[control.control_id] ? ' selected' : ''}>${window.escapeHtml(window.renderOptionLabelWithGloss(option, locale))}</option>`).join('')}
      </select>
    </label>
  `).join('');
  const initialComputed = window.computePatternBuilderOutput(builder, initialResolvedValues);

  return `
    <div class="content-block">
      <div class="block-title">${window.escapeHtml(window.i18nText(builder.title_i18n, locale, builder.title_zh_tw || '可切換句型'))}</div>
      <div id="${builderId}" class="summary-box" data-builder-config="${configJsonAttr}">
        ${window.i18nText(builder.inline_hint_i18n, locale, '') ? `<div class="muted-text" style="margin-bottom:12px;">${window.escapeHtml(window.i18nText(builder.inline_hint_i18n, locale, ''))}</div>` : ''}
        <div class="summary-grid" style="grid-template-columns:repeat(3, 1fr);">
          ${controlsHtml}
        </div>
        <div class="pattern-entry" style="margin-top:8px;">
          <div style="display:flex; align-items:center; gap:8px;">
            <div class="pattern-formula" data-builder-output style="flex:1;">${window.escapeHtml(initialComputed.sentence)}</div>
            ${window.ttsSupported && window.ttsSupported() ? `<button class="btn tiny-text" data-builder-speak data-tts-text="${window.escapeHtml(initialComputed.sentence)}" onclick="event.stopPropagation(); window.speakKo(this.getAttribute('data-tts-text') || ''); return false;" title="播放目前句子" style="padding:4px 8px;">▶</button>` : ''}
          </div>
          <div class="pattern-use-case" data-builder-gloss>${window.escapeHtml(initialComputed.gloss)}</div>
        </div>
      </div>
    </div>
  `;
};

window.renderLessonSupportModule = function (module) {
  if (!module) return '';
  const locale = currentLocale();
  const items = (module.items || []).map(item => `
    <div class="pro-item">
      <strong>${window.escapeHtml(item.target || '')}</strong>
      ${window.i18nText(item.explain_i18n, locale, '') ? `<div class="tiny-text muted" style="margin-top:3px;">${window.escapeHtml(window.i18nText(item.explain_i18n, locale, ''))}</div>` : ''}
    </div>
  `).join('');

  return `
    <div class="content-block">
      <div class="block-title">${window.escapeHtml(window.i18nText(module.title_i18n, locale, '語體怎麼選'))}</div>
      ${window.i18nText(module.why_here_i18n, locale, '') ? `<div class="muted-text" style="margin-bottom:12px;">${window.escapeHtml(window.i18nText(module.why_here_i18n, locale, ''))}</div>` : ''}
      <div class="compare-pros">${items}</div>
    </div>
  `;
};

const renderDialogue = function (payload, node) {
  const locale = currentLocale();
  const turns = payload.dialogue_turns || [];
  const scenes = payload.dialogue_scenes || [];
  if (!payload.dialogue_turns && !payload.dialogue_scenes) return window.RendererRegistry.renderMalformedPayload('dialogue', 'none', ['dialogue_turns']);

  let coachIntro = '';
  if (window.i18nText(payload.coach_intro_i18n, locale, '')) {
    coachIntro = `
      <div class="content-block">
        <div class="block-title">朋友先跟你講重點</div>
        <div class="summary-box" style="background:var(--accent-soft); border-color:var(--accent-soft);">
          ${window.escapeHtml(window.i18nText(payload.coach_intro_i18n, locale, ''))}
        </div>
      </div>
    `;
  }

  let whatToNotice = '';
  if (payload.what_to_notice_i18n && payload.what_to_notice_i18n.length) {
    const items = payload.what_to_notice_i18n.map(item => `
      <div class="pro-item">
        ${window.escapeHtml(window.i18nText(item, locale, ''))}
      </div>
    `).join('');
    whatToNotice = `<div class="content-block"><div class="block-title">這段先注意什麼</div><div class="compare-pros">${items}</div></div>`;
  }

  const renderTurns = function (sceneTurns) {
    return sceneTurns.map((t, idx) => {
      const isRight = idx % 2 !== 0;
      return `
        <div class="dialogue-turn ${isRight ? 'turn-right' : 'turn-left'}">
          <div class="speaker-label">${window.escapeHtml(t.speaker)}</div>
          <div class="bubble">
            <div class="bubble-ko">${window.escapeHtml(t.text)} ${window.renderSpeakButton(t.text)}</div>
            ${window.showBilingual() && (window.i18nText(t.translations_i18n, locale, '') || t.zh_tw) ? `<div class="bubble-zh">${window.escapeHtml(window.i18nText(t.translations_i18n, locale, t.zh_tw || ''))}</div>` : ''}
          </div>
        </div>
      `;
    }).join('');
  };

  const html = scenes.length
    ? scenes.map(scene => `
        <div class="content-block" style="margin:0 0 14px 0;">
          <div class="block-title">${window.escapeHtml(window.i18nText(scene.title_i18n, locale, scene.title_zh_tw || scene.title || '短對話'))}</div>
          ${window.i18nText(scene.note_i18n, locale, scene.note_zh_tw || '') ? `<div class="muted-text" style="margin-bottom:10px;">${window.escapeHtml(window.i18nText(scene.note_i18n, locale, scene.note_zh_tw || ''))}</div>` : ''}
          <div class="dialogue-wrap">${renderTurns(scene.turns || [])}</div>
        </div>
      `).join('')
    : renderTurns(turns);

  let registerSwitch = '';
  if (payload.register_switch_bank && payload.register_switch_bank.length) {
    const rows = payload.register_switch_bank.map(row => `
      <div class="pattern-entry">
        <div class="tiny-text muted" style="margin-bottom:6px; font-weight:700;">${window.escapeHtml(window.i18nText(row.meaning_i18n, locale, ''))}</div>
        <div class="summary-grid">
          <div class="summary-box"><span class="label">正式</span>${window.escapeHtml(row.formal || '')}</div>
          <div class="summary-box"><span class="label">日常</span>${window.escapeHtml(row.polite || '')}</div>
          <div class="summary-box"><span class="label">朋友</span>${window.escapeHtml(row.casual || '')}</div>
        </div>
        ${window.i18nText(row.note_i18n, locale, '') ? `<div class="tiny-text muted" style="margin-top:8px;">${window.escapeHtml(window.i18nText(row.note_i18n, locale, ''))}</div>` : ''}
      </div>
    `).join('');
    registerSwitch = `<div class="content-block"><div class="block-title">三種禮貌等級切換</div>${rows}</div>`;
  }

  let patternBuilder = '';
  if (payload.pattern_builder_demos && payload.pattern_builder_demos.length) {
    patternBuilder = payload.pattern_builder_demos.map(builder => window.renderPatternBuilderBlock(builder, node && (node.id || node.node_id))).join('');
  } else if (payload.pattern_builder_demo) {
    patternBuilder = window.renderPatternBuilderBlock(payload.pattern_builder_demo, node && (node.id || node.node_id));
  }

  const lessonSupportModule = window.renderLessonSupportModule(payload.lesson_support_module || null);

  return `${coachIntro}${whatToNotice}<div class="content-block"><div class="block-title">情境對話</div>${scenes.length ? html : `<div class="dialogue-wrap">${html}</div>`}</div>${lessonSupportModule}${registerSwitch}${patternBuilder}`;
};

const renderPatternLab = function (payload, node) {
  const locale = currentLocale();
  let patternBuilder = '';
  if (payload.pattern_builder_demos && payload.pattern_builder_demos.length) {
    patternBuilder = payload.pattern_builder_demos.map(builder => window.renderPatternBuilderBlock(builder, node && (node.id || node.node_id))).join('');
  } else if (payload.pattern_builder_demo) {
    patternBuilder = window.renderPatternBuilderBlock(payload.pattern_builder_demo, node && (node.id || node.node_id));
  }

  const lessonSupportModule = window.renderLessonSupportModule(payload.lesson_support_module || null);
  const slotBanks = (payload.slot_bank_panels || []).map(panel => `
    <div class="content-block">
      <div class="block-title">${window.escapeHtml(window.i18nText(panel.title_i18n, locale, '可替換材料'))}</div>
      <div class="compare-pros">
        ${(panel.items_i18n || []).map(item => `
          <div class="pro-item">
            <strong>${window.escapeHtml(item.ko || '')}</strong>
            <div class="tiny-text muted" style="margin-top:3px;">${window.escapeHtml(window.i18nText(item, locale, item.zh_tw || ''))}</div>
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');
  return `${lessonSupportModule}${slotBanks}${patternBuilder}`;
};

const renderNotice = function (payload) {
  const locale = currentLocale();
  const items = payload.notice_items || [];
  const itemZh = payload.notice_items_zh_tw || [];
  const itemI18n = payload.notice_items_i18n || [];
  const blockTitle = window.i18nText(payload.block_title_i18n, locale, '告示與看板');
  if (!payload.notice_items) return window.RendererRegistry.renderMalformedPayload('notice', 'none', ['notice_items']);

  const html = items.map((ko, idx) => `
    <div class="notice-item">
      <span class="notice-ko">${window.escapeHtml(ko)} ${window.renderSpeakButton(ko)}</span>
      ${window.showBilingual() && (window.i18nText(itemI18n[idx], locale, '') || itemZh[idx]) ? `<span class="notice-zh">${window.escapeHtml(window.i18nText(itemI18n[idx], locale, itemZh[idx] || ''))}</span>` : ''}
    </div>
  `).join('');
  return `<div class="content-block"><div class="block-title">${window.escapeHtml(blockTitle)}</div><div class="notice-board">${html}</div></div>`;
};

const renderMessageThread = function (payload) {
  const msgs = payload.messages || [];
  if (!payload.messages) return window.RendererRegistry.renderMalformedPayload('message_thread', 'none', ['messages']);

  const html = msgs.map((m, idx) => {
    const isMe = typeof m.is_self === 'boolean' ? m.is_self : idx % 2 === 0;
    return `
      <div class="msg-group ${isMe ? 'msg-right' : 'msg-left'}">
        <div class="msg-sender">${window.escapeHtml(m.sender)}</div>
        <div class="msg-bubble">
          <div class="msg-ko">${window.escapeHtml(m.text)} ${window.renderSpeakButton(m.text)}</div>
          ${window.showBilingual() && m.zh_tw ? `<div class="msg-zh">${window.escapeHtml(m.zh_tw)}</div>` : ''}
        </div>
      </div>
    `;
  }).join('');
  return `<div class="content-block"><div class="block-title">簡訊對話</div><div class="message-container">${html || '<div class="empty-state">無訊息</div>'}</div></div>`;
};

const renderComparison = function (payload) {
  const opts = payload.options || [];
  if (!payload.options) return window.RendererRegistry.renderMalformedPayload('comparison_card', 'none', ['options']);

  const html = opts.map(o => `
    <div class="compare-card">
      <span class="card-id">${o.id}</span>
      <h4>
        ${window.escapeHtml(o.label_ko || o.label_zh_tw || '')}
        ${(window.showBilingual() && o.label_zh_tw && o.label_ko) ? `<div class="tiny-text muted" style="font-weight:500; margin-top:4px;">${window.escapeHtml(o.label_zh_tw)}</div>` : ''}
      </h4>
      <div class="price-tag">${(o.price_krw || 0).toLocaleString()} KRW</div>
      <div class="compare-pros">
        ${(o.pros_ko || o.pros_zh_tw || []).map((p, idx) => `
          <div class="pro-item">
            ${window.escapeHtml(p)}
            ${(window.showBilingual() && o.pros_ko && o.pros_zh_tw && o.pros_zh_tw[idx]) ? `<div class="tiny-text muted" style="margin-top:2px;">${window.escapeHtml(o.pros_zh_tw[idx])}</div>` : ''}
          </div>
        `).join('')}
      </div>
    </div>
  `).join('');

  let frameNote = '';
  if (payload.reason_frame_ko || payload.reason_frame_zh_tw) {
    frameNote = `<div class="summary-box" style="margin-top:20px; border-style:solid; border-color:var(--accent2-soft); background:var(--accent2-soft);">
      <span class="label" style="color:var(--accent2);">推薦理由句型</span>
      ${window.escapeHtml(payload.reason_frame_ko || payload.reason_frame_zh_tw || '')}
      ${(window.showBilingual() && payload.reason_frame_ko && payload.reason_frame_zh_tw) ? `<div class="tiny-text muted" style="margin-top:4px;">${window.escapeHtml(payload.reason_frame_zh_tw)}</div>` : ''}
    </div>`;
  }

  return `<div class="content-block"><div class="block-title">方案比較</div><div class="comparison-grid">${html}</div>${frameNote}</div>`;
};

const renderPatternCard = function (payload) {
  const locale = currentLocale();
  const frames = payload.frames || [];
  const html = frames.map(f => `
    <div class="pattern-entry">
      <div class="pattern-formula">${window.escapeHtml(f.frame)}</div>
      <div class="pattern-use-case">${window.escapeHtml(window.i18nText(f.use_i18n, locale, f.use_zh_tw || ''))}</div>
      <div class="slot-tags">
        <span class="slot-label">詞類/插槽:</span>
        ${((f.slots_i18n || []).length ? f.slots_i18n.map(s => window.i18nText(s, locale)) : (f.slots_zh_tw || [])).map(s => `<span class="slot-tag">${window.escapeHtml(s)}</span>`).join('')}
      </div>
    </div>
  `).join('');
  return `<div class="content-block"><div class="block-title">句型重點</div><div class="pattern-card-box">${html || '<div class="empty-state">無資料</div>'}</div></div>`;
};

const renderPracticeCardHead = function (payload, node) {
  const locale = currentLocale();
  const modeLabel = {
    chunk_assembly: '拼句型練習',
    response_builder: '回應建構',
    guided: '引導式練習'
  }[payload.mode || node.output_mode] || '練習卡';

  const taskCount = Array.isArray(payload.tasks) ? payload.tasks.length : 0;
  const itemCount = Array.isArray(payload.items) ? payload.items.length : 0;
  const total = taskCount || itemCount;

  return `
    <div class="card-block animate-in">
      <div class="block-title">Practice Card</div>
      <div class="muted-text" style="margin-bottom:10px;">${window.escapeHtml(modeLabel)}</div>
      ${window.i18nText(payload.prompt_i18n, locale, payload.prompt_zh_tw || '') ? `<div style="margin-bottom:10px;">${window.escapeHtml(window.i18nText(payload.prompt_i18n, locale, payload.prompt_zh_tw || ''))}</div>` : ''}
      ${total ? `<div class="tiny-text muted">本節練習題數：${total}</div>` : ''}
      <div class="tiny-text muted" style="margin-top:8px;">互動內容請見下方練習區塊。</div>
    </div>
  `;
};

const renderComprehensionCheck = function (payload) {
  const locale = currentLocale();
  const items = payload.items || [];
  const qType = payload.question_type || 'unknown';
  const html = items.map((item, idx) => `
    <div class="pattern-entry">
      <div class="tiny-text muted">題目 ${idx + 1}</div>
      <div style="font-weight:600; margin:4px 0 8px;">${window.escapeHtml(window.i18nText(item.prompt_i18n, locale, item.prompt_zh_tw || item.prompt_ko || ''))}</div>
      ${(item.response_choices_ko || []).length ? `
        <div class="chip-cloud">
          ${(item.response_choices_ko || []).map(c => `
            <span class="word-chip">
              ${window.escapeHtml(c)}
              ${window.renderSpeakInline(c)}
              ${window.showBilingual() && item.response_gloss_by_ko && item.response_gloss_by_ko[c] ? `
                <span class="tiny-text muted" style="display:block; margin-top:3px;">${window.escapeHtml(item.response_gloss_by_ko[c])}</span>
              ` : ''}
            </span>
          `).join('')}
        </div>
      ` : ''}
    </div>
  `).join('');

  return `
    <div class="content-block">
      <div class="block-title">理解檢核</div>
      <div class="tiny-text muted" style="margin-bottom:10px;">題型：${window.escapeHtml(qType)}</div>
      <div class="pattern-card-box">${html || '<div class="empty-state">無題目資料</div>'}</div>
    </div>
  `;
};

const renderRoleplayPrompt = function (payload) {
  const locale = currentLocale();
  return `
    <div class="card-block animate-in">
      <div class="block-title">Roleplay Prompt</div>
      ${payload.scenery_ko ? `
        <div style="margin-bottom:8px;">
          <div class="tiny-text muted">情境（韓文）</div>
          <div>${window.escapeHtml(payload.scenery_ko)}</div>
          ${window.showBilingual() && window.i18nText(payload.scenery_i18n, locale, payload.scenery_zh_tw || '') ? `<div class="tiny-text muted" style="margin-top:4px;">${window.escapeHtml(window.i18nText(payload.scenery_i18n, locale, payload.scenery_zh_tw || ''))}</div>` : ''}
        </div>` : ''
    }
      ${(Array.isArray(payload.constraints_i18n) && payload.constraints_i18n.length) || (Array.isArray(payload.constraints_zh_tw) && payload.constraints_zh_tw.length) ? `
        <div style="margin-bottom:8px;">
          <div class="tiny-text muted">限制條件</div>
          <ul style="margin:6px 0 0 18px;">${((payload.constraints_i18n || []).length ? payload.constraints_i18n.map(v => window.i18nText(v, locale)) : payload.constraints_zh_tw).map(v => `<li>${window.escapeHtml(v)}</li>`).join('')}</ul>
        </div>` : ''
    }
      ${(Array.isArray(payload.required_patterns_i18n) && payload.required_patterns_i18n.length) || (Array.isArray(payload.required_patterns_zh_tw) && payload.required_patterns_zh_tw.length) ? `
        <div>
          <div class="tiny-text muted">必用句型</div>
          <div class="chip-cloud" style="margin-top:6px;">
            ${((payload.required_patterns_i18n || []).length ? payload.required_patterns_i18n.map(v => window.i18nText(v, locale)) : payload.required_patterns_zh_tw).map(v => `<span class="word-chip">${window.escapeHtml(v)}</span>`).join('')}
          </div>
        </div>` : ''
    }
    </div>
  `;
};

const renderMessagePrompt = function (payload) {
  return `
    <div class="card-block animate-in">
      <div class="block-title">Message Prompt</div>
      ${payload.prompt_ko ? `<div style="font-weight:700;">${window.escapeHtml(payload.prompt_ko)}</div>` : ''}
      ${window.showBilingual() && payload.prompt_zh_tw ? `<div class="tiny-text muted" style="margin-top:6px;">${window.escapeHtml(payload.prompt_zh_tw)}</div>` : ''}
      ${Array.isArray(payload.must_include_zh_tw) && payload.must_include_zh_tw.length ? `
        <div style="margin-top:10px;">
          <div class="tiny-text muted">需包含</div>
          <ul style="margin:6px 0 0 18px;">${payload.must_include_zh_tw.map(v => `<li>${window.escapeHtml(v)}</li>`).join('')}</ul>
        </div>` : ''
    }
      ${Array.isArray(payload.example_shape_ko) && payload.example_shape_ko.length ? `
        <div style="margin-top:10px;">
          <div class="tiny-text muted">句型輪廓</div>
          ${(payload.example_shape_ko || []).map((ko, i) => `
            <div style="padding:8px 10px; background:#faf7f1; border-radius:8px; margin-top:6px;">
              <div>${window.escapeHtml(ko)}</div>
              ${window.showBilingual() && payload.example_shape_zh_tw && payload.example_shape_zh_tw[i] ? `<div class="tiny-text muted">${window.escapeHtml(payload.example_shape_zh_tw[i])}</div>` : ''}
            </div>
          `).join('')}
        </div>` : ''
    }
    </div>
  `;
};

const renderReviewCard = function (payload) {
  const locale = currentLocale();
  const prompts = (payload.prompts_i18n || []).length ? payload.prompts_i18n.map(v => window.i18nText(v, locale)) : (payload.prompts_zh_tw || []);
  return `
    <div class="card-block animate-in">
      <div class="block-title">Review Card</div>
      <div class="muted-text" style="margin-bottom:8px;">先回想，再用下方互動區塊檢視提示與答案。</div>
      ${payload.hint_policy ? `<div class="tiny-text muted" style="margin-bottom:8px;">提示策略：${window.escapeHtml(payload.hint_policy)}</div>` : ''}
      ${prompts.length ? `
        <ol style="margin:0 0 0 18px; padding:0;">
          ${prompts.map(p => `<li style="margin-bottom:6px;">${window.escapeHtml(p)}</li>`).join('')}
        </ol>` : ''
    }
    </div>
  `;
};

const renderQuizItem = function (payload) {
  const item = payload.item || {};
  const choices = Array.isArray(item.choices) ? item.choices : [];
  const answer = item.answer_key ? item.answer_key.value : '';
  const answerText = Array.isArray(answer) ? answer.join(' / ') : String(answer || '');
  return `
    <div class="content-block">
      <div class="block-title">題庫題目</div>
      <div class="summary-box" style="margin-bottom:12px;">
        <span class="label">題型 / 技能 / 難度</span>
        ${window.escapeHtml(item.item_type || 'unknown')} / ${window.escapeHtml(item.skill || 'unknown')} / ${window.escapeHtml(item.difficulty_tier || 'L1')}
      </div>
      <div style="font-weight:700; margin-bottom:6px;">${window.escapeHtml(item.prompt_zh_tw || '')}</div>
      ${item.prompt_ko ? `<div style="padding:10px; background:#fff; border:1px solid var(--line); border-radius:8px; margin-bottom:10px;">
        <div style="font-size:16px; font-weight:700;">${window.escapeHtml(item.prompt_ko)} ${window.renderSpeakButton(item.prompt_ko)}</div>
      </div>` : ''}
      ${choices.length ? `
        <div class="chip-cloud" style="margin-bottom:10px;">
          ${choices.map((c, idx) => `<span class="word-chip">${idx + 1}. ${window.escapeHtml(c)} ${window.renderSpeakInline(c)}</span>`).join('')}
        </div>
      ` : ''}
      <details>
        <summary style="cursor:pointer; color:var(--accent2); font-weight:700;">顯示答案與解析</summary>
        <div class="summary-box" style="margin-top:8px; border-color:var(--ok-soft); background:var(--ok-soft);">
          <span class="label" style="color:var(--ok);">答案</span>
          ${window.escapeHtml(answerText)}
          ${item.explanation_zh_tw ? `<div class="tiny-text muted" style="margin-top:6px;">${window.escapeHtml(item.explanation_zh_tw)}</div>` : ''}
        </div>
      </details>
      ${item.tags?.length ? `<div class="tiny-text muted" style="margin-top:10px;">tags: ${item.tags.map(t => window.escapeHtml(t)).join(', ')}</div>` : ''}
    </div>
  `;
};

const applyInlineMarkdown = function (text) {
  return window.escapeHtml(text || '')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`([^`]+)`/g, '<code>$1</code>');
};

const markdownToHtmlLite = function (md) {
  const src = String(md || '').replace(/\r\n/g, '\n');
  const lines = src.split('\n');
  const out = [];
  let i = 0;

  const isTableSeparator = (line) => /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
  const isTableRow = (line) => line.includes('|');

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    if (!trimmed) {
      i += 1;
      continue;
    }

    // Table block
    if (i + 1 < lines.length && isTableRow(lines[i]) && isTableSeparator(lines[i + 1])) {
      const headerCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
      i += 2;
      const bodyRows = [];
      while (i < lines.length && isTableRow(lines[i]) && lines[i].trim()) {
        const rowCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
        if (rowCells.length) bodyRows.push(rowCells);
        i += 1;
      }
      out.push(`
        <div class="md-table-wrap">
          <table class="md-table">
            <thead><tr>${headerCells.map(c => `<th>${applyInlineMarkdown(c)}</th>`).join('')}</tr></thead>
            <tbody>${bodyRows.map(r => `<tr>${r.map(c => `<td>${applyInlineMarkdown(c)}</td>`).join('')}</tr>`).join('')}</tbody>
          </table>
        </div>
      `);
      continue;
    }

    // Bullet list
    if (trimmed.startsWith('- ')) {
      const items = [];
      while (i < lines.length && lines[i].trim().startsWith('- ')) {
        items.push(lines[i].trim().slice(2));
        i += 1;
      }
      out.push(`<ul class="grammar-point-list">${items.map(p => `<li>${applyInlineMarkdown(p)}</li>`).join('')}</ul>`);
      continue;
    }

    // Paragraph
    out.push(`<p class="md-paragraph">${applyInlineMarkdown(trimmed)}</p>`);
    i += 1;
  }

  return out.join('');
};

const renderGrammar = function (payload) {
  const locale = currentLocale();
  const sections = payload.sections || [];
  const html = sections.map(s => `
    <details open>
      <summary>${window.escapeHtml(window.i18nText(s.title_i18n, locale, s.title_zh_tw || ''))}</summary>
      <div class="grammar-body">
        ${window.i18nText(s.explanation_md_i18n, locale, s.explanation_md || '')
      ? `<div class="md-block">${markdownToHtmlLite(window.i18nText(s.explanation_md_i18n, locale, s.explanation_md || ''))}</div>`
      : `<ul class="grammar-point-list">
              ${(((s.points_i18n || []).length ? s.points_i18n.map(p => window.i18nText(p, locale)) : (s.points_zh_tw || []))).map(p => `<li>${window.escapeHtml(p)}</li>`).join('')}
            </ul>`
    }
      </div>
    </details>
  `).join('');
  return `<div class="content-block"><div class="block-title">文法詳解</div><div class="grammar-accordion">${html || '<div class="empty-state">無資料</div>'}</div></div>`;
};

const renderDictionary = function (payload) {
  const sections = payload.sections || [];
  const html = sections.map(s => {
    const gloss = s.item_gloss_by_ko || {};
    return `
      <div class="dict-section">
        <span class="dict-box-title">${window.escapeHtml(s.title_zh_tw)}</span>
        <div class="chunk-cloud">
          ${(s.items || []).map(it => `
            <div class="cloud-chunk">
              <strong>${window.escapeHtml(it)}</strong> ${window.renderSpeakButton(it)}
              ${window.showBilingual() && gloss[it] ? `<span class="chunk-zh">${window.escapeHtml(gloss[it])}</span>` : ''}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }).join('');
  return `<div class="content-block"><div class="block-title">核心詞彙與短語</div><div>${html || '<div class="empty-state">無資料</div>'}</div></div>`;
};

// --- Interaction Mode implement functions ---

const renderChunkAssemblyMode = function (node) {
  const payload = node.payload;
  const nodeState = window.getNodeInteractionState(node.id);
  const tasks = payload.tasks || [];
  if (!tasks.length) {
    return `
      <div class="interaction-panel">
        <div class="interaction-label">ℹ️ 本節無互動題</div>
        <div class="muted-text">此節點目前是內容瀏覽模式，未提供可操作的 chunk_assembly tasks。</div>
      </div>
    `;
  }
  const shuffleArray = (arr) => {
    const next = [...arr];
    for (let i = next.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [next[i], next[j]] = [next[j], next[i]];
    }
    return next;
  };
  if (!Array.isArray(nodeState.taskOrder) || nodeState.taskOrder.length !== tasks.length) {
    const order = shuffleArray(tasks.map((_, idx) => idx));
    nodeState.taskOrder = order;
    nodeState.chunkOrderByTaskIndex = Object.fromEntries(
      tasks.map((task, idx) => [idx, shuffleArray(task.chunks || [])])
    );
    nodeState.activeTaskIndex = 0;
    window.setNodeInteractionState(node.id, nodeState);
  }
  const order = nodeState.taskOrder || tasks.map((_, idx) => idx);
  const taskIdx = Math.max(0, Math.min(nodeState.activeTaskIndex || 0, tasks.length - 1));
  if (taskIdx !== (nodeState.activeTaskIndex || 0)) {
    nodeState.activeTaskIndex = taskIdx;
    window.setNodeInteractionState(node.id, nodeState);
  }
  const task = tasks[order[taskIdx]];
  if (!task) {
    return `
      <div class="interaction-panel">
        <div class="interaction-label">ℹ️ 本節無互動題</div>
        <div class="muted-text">此節點目前是內容瀏覽模式，未提供可操作的 chunk_assembly tasks。</div>
      </div>
    `;
  }

  const currentAnswers = nodeState.answers || [];
  const assembled = currentAnswers.join(' ').trim();
  const chunkOrder = Array.isArray(nodeState.chunkOrderByTaskIndex?.[order[taskIdx]])
    ? nodeState.chunkOrderByTaskIndex[order[taskIdx]]
    : shuffleArray(task.chunks || []);
  const targets = task.target_examples || [];
  const acceptable = task.acceptable_examples || [];
  const feedbackState = nodeState.feedbackByTaskIndex?.[order[taskIdx]] || null;

  const answerHtml = currentAnswers.map((a, i) => `
    <div class="chip" onclick="removeChunk(${i})">
      ${window.escapeHtml(a)} ${window.renderSpeakButton(a)}
    </div>
  `).join('');

  const bankHtml = chunkOrder.map((c) => {
    const usedCount = currentAnswers.filter(x => x === c).length;
    const totalCount = (task.chunks || []).filter(x => x === c).length;
    const isUsed = usedCount >= totalCount;
    return `<div class="chip ${isUsed ? 'used' : ''}" onclick="${isUsed ? '' : `addChunk('${c.replace(/'/g, "\\'")}')`}">
      ${window.escapeHtml(c)} ${window.renderSpeakButton(c)}
    </div>`;
  }).join('');

  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🧩 詞塊組句練習 (${taskIdx + 1}/${tasks.length})</div>
      ${task.context_zh_tw ? `<div class="summary-box" style="margin-bottom:10px; background:#fff9ee; border-color:#f1dfb7;"><span class="label">場合</span>${window.escapeHtml(task.context_zh_tw)}</div>` : ''}
      <div class="muted-text" style="margin-bottom:12px;">${window.escapeHtml(task.prompt_zh_tw || '')}</div>
      
      <div class="assembly-zone">
        <div class="block-title" style="margin-bottom:8px; font-size:11px;">你的組句 (點擊移除)</div>
        <div class="assembly-answer">${answerHtml || '<div class="tiny-text muted">請從下方選擇詞塊...</div>'}</div>
        
        <div class="block-title" style="margin-bottom:8px; font-size:11px; margin-top:16px;">詞塊庫</div>
        <div class="chunk-cloud">${bankHtml}</div>
      </div>

      <div class="btn-row">
        <button class="btn" onclick="clearAssembly()">清空</button>
        <button class="btn" onclick="checkAssembly()">檢查</button>
        <button class="btn" onclick="toggleTaskExample()">查看示例</button>
        <button class="btn primary" onclick="nextTask()">${taskIdx >= tasks.length - 1 ? '再來一輪' : '下一題'}</button>
      </div>
      ${feedbackState ? `
        <div class="summary-box" style="margin-top:12px; border-color:${feedbackState.kind === 'best_fit' ? 'var(--ok-soft)' : feedbackState.kind === 'acceptable_but_less_natural' ? '#f1dfb7' : '#f3d0d0'}; background:${feedbackState.kind === 'best_fit' ? 'var(--ok-soft)' : feedbackState.kind === 'acceptable_but_less_natural' ? '#fff9ee' : '#fff3f3'};">
          <span class="label" style="color:${feedbackState.kind === 'best_fit' ? 'var(--ok)' : feedbackState.kind === 'acceptable_but_less_natural' ? '#8a6500' : '#b42318'};">
            ${feedbackState.kind === 'best_fit' ? '最自然' : feedbackState.kind === 'acceptable_but_less_natural' ? '文法可通' : '再調整'}
          </span>
          ${window.escapeHtml(feedbackState.message)}
          ${feedbackState.answer ? `<div class="tiny-text muted" style="margin-top:6px;">你現在組的是：${window.escapeHtml(feedbackState.answer)}</div>` : ''}
        </div>
      ` : ''}
      <div id="assemblyExample" class="summary-box" style="display:none; margin-top:16px; border-color:var(--ok-soft); background:var(--ok-soft);">
        <span class="label" style="color:var(--ok);">預期示例</span>
        ${(task.target_examples || []).join(' / ')}
        ${window.showBilingual() && task.target_examples_zh_tw ? `<div class="tiny-text" style="margin-top:4px;">中譯：${task.target_examples_zh_tw.join(' / ')}</div>` : ''}
      </div>
    </div>
  `;
};

const renderResponseBuilderMode = function (node) {
  const items = node.payload.items || [];
  const nodeState = window.getNodeInteractionState(node.id);
  const chosen = nodeState.chosenByIndex || {};
  if (!node.payload.items) return window.RendererRegistry.renderMalformedPayload('practice_card', 'response_builder', ['items']);

  const html = items.map((item, idx) => `
      <div style="margin-bottom:24px; border-bottom:1px dashed var(--line); padding-bottom:16px;">
      <div class="muted-text" style="font-weight:700; margin-bottom:8px;">情境 ${idx + 1}: ${window.escapeHtml(item.prompt_ko)} ${window.renderSpeakButton(item.prompt_ko)}</div>
      ${window.showBilingual() && item.prompt_zh_tw ? `<div class="tiny-text muted" style="margin-bottom:12px;">(${item.prompt_zh_tw})</div>` : ''}
      <div class="btn-group" style="flex-wrap:wrap;">
        ${(item.response_choices_ko || []).map(choice => `
          <button class="btn ${chosen[idx] === choice ? 'success' : ''}" style="font-size:12px; padding: 6px 12px;" onclick="pickResponse(${idx}, '${choice.replace(/'/g, "\\'")}')">
            ${window.escapeHtml(choice)} ${window.renderSpeakInline(choice)}
            ${window.showBilingual() && item.response_gloss_by_ko && item.response_gloss_by_ko[choice] ? `<span class="tiny-text muted" style="display:block; width:100%; margin-top:2px;">${window.escapeHtml(item.response_gloss_by_ko[choice])}</span>` : ''}
          </button>
        `).join('')}
      </div>
    </div>
  `).join('');

  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">💬 回應選擇練習</div>
      ${html}
    </div>
  `;
};

const renderGuidedOutputMode = function (node) {
  const locale = currentLocale();
  const nodeState = window.getNodeInteractionState(node.id);
  const isSpeaking = (node.skill_focus || []).includes('speaking');
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">${isSpeaking ? '🎤 口說練習' : '✍️ 任務型寫作'}</div>
      <div class="muted-text" style="margin-bottom:12px;">${window.escapeHtml(window.i18nText(node.payload.prompt_i18n, locale, node.payload.prompt_zh_tw || window.i18nText(node.summary_i18n, locale, node.summary_zh_tw || '')))}</div>
      <textarea placeholder="點擊此處輸入回答或練習筆記..." oninput="updateDraft(this.value)">${nodeState.draft || ''}</textarea>
      ${node.payload.must_include_zh_tw ? `<div class="tiny-text muted" style="margin-top:8px;">需包含: ${node.payload.must_include_zh_tw.join(' / ')}</div>` : ''}
    </div>
  `;
};

const renderFrameFillMode = function (node) {
  const locale = currentLocale();
  const frames = node.payload?.frames || [];
  if (!frames.length) {
    return `
      <div class="interaction-panel">
        <div class="interaction-label">ℹ️ Frame Fill</div>
        <div class="muted-text">此節點未提供 frames，請先檢查 payload.frames。</div>
      </div>
    `;
  }
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🧩 句框填空練習</div>
      ${frames.map((f, idx) => `
        <div style="margin-top:10px; padding:10px; background:#fff; border:1px solid var(--line); border-radius:8px;">
          <div class="tiny-text muted">Frame ${idx + 1}</div>
          <div style="font-weight:700; margin:4px 0;">${window.escapeHtml(f.frame || '')}</div>
          ${window.i18nText(f.use_i18n, locale, f.use_zh_tw || '') ? `<div class="tiny-text muted">${window.escapeHtml(window.i18nText(f.use_i18n, locale, f.use_zh_tw || ''))}</div>` : ''}
        </div>
      `).join('')}
      <div class="tiny-text muted" style="margin-top:10px;">先口頭替換 slot，再到筆記區寫一版完整句子。</div>
    </div>
  `;
};

const renderPatternTransformMode = function (node) {
  const locale = currentLocale();
  const payload = node.payload || {};
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🔁 句型變換練習</div>
      <div class="tiny-text muted">Transform Type: ${window.escapeHtml(payload.transform_type || 'unspecified')}</div>
      <div style="margin-top:8px;">${window.escapeHtml(window.i18nText(payload.prompt_i18n, locale, payload.prompt_zh_tw || window.i18nText(node.summary_i18n, locale, node.summary_zh_tw || '請根據本節句型完成變換。')))}</div>
      ${(payload.must_include_zh_tw || []).length ? `
        <div style="margin-top:8px;">
          <div class="tiny-text muted">必含元素</div>
          <div class="chip-cloud">${payload.must_include_zh_tw.map(v => `<span class="word-chip">${window.escapeHtml(v)}</span>`).join('')}</div>
        </div>
      ` : ''}
    </div>
  `;
};

const renderReviewRetrievalMode = function (node) {
  const prompts = node.payload.prompts_zh_tw || [];
  const answers = node.payload.reference_answers_ko || node.payload.answers_ko || [];
  const nodeState = window.getNodeInteractionState(node.id);
  const retrievalDrafts = nodeState.retrievalDrafts || {};
  const revealedHints = nodeState.revealedHints || {};
  const revealedAnswers = nodeState.revealedAnswers || {};
  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🧠 單元複習回想</div>
      <div class="muted-text" style="margin-bottom:16px;">閱讀以下情境，先自己回想，再決定是否查看提示與答案（不自動評分）。</div>
      ${prompts.map((p, i) => `
        <div style="margin-bottom:12px; padding:12px; background:#fff; border-radius:8px; border:1px solid var(--line);">
          <div class="tiny-text muted">情境 ${i + 1}</div>
          <div>${window.escapeHtml(p)}</div>
          <textarea style="margin-top:10px; min-height:70px;" placeholder="先寫下你回想的答案..." oninput="updateRetrievalDraft(${i}, this.value)">${window.escapeHtml(retrievalDrafts[i] || '')}</textarea>
          <div class="btn-group" style="margin-top:8px; gap:6px; flex-wrap:wrap;">
            <button class="btn tiny-text" style="padding:4px 10px;" onclick="toggleRetrievalHint(${i})">${revealedHints[i] ? '隱藏提示' : '顯示提示'}</button>
            <button class="btn tiny-text" style="padding:4px 10px;" onclick="toggleRetrievalAnswer(${i})">${revealedAnswers[i] ? '隱藏答案' : '顯示答案'}</button>
          </div>
          ${revealedHints[i] ? `<div class="tiny-text muted" style="margin-top:8px; padding:8px; background:#faf7f1; border-radius:6px;">提示：先回想本單元的功能句型（點餐請求 / 回應店員 / 付款 / 約見）。</div>` : ''}
          ${revealedAnswers[i] ? `<div style="margin-top:8px; padding:8px; background:#eef8f0; border:1px solid #d0e6d6; border-radius:6px;"><div class="tiny-text muted">參考答案（韓文）</div><div style="font-weight:600;">${window.escapeHtml(answers[i] || '尚未定義')} ${answers[i] ? window.renderSpeakButton(answers[i]) : ''}</div></div>` : ''}
        </div>
      `).join('')}
    </div>
  `;
};

const renderFlashcardReviewMode = function (node) {
  const locale = currentLocale();
  const payload = node.payload || {};
  const cards = payload.cards || [];
  if (!cards.length) {
    return `
      <div class="interaction-panel">
        <div class="interaction-label">ℹ️ Flashcard Review</div>
        <div class="muted-text">此節點未提供 cards，請先檢查 payload.cards。</div>
      </div>
    `;
  }
  const nodeState = window.getNodeInteractionState(node.id);
  const cardOrder = Array.isArray(nodeState.cardOrder) && nodeState.cardOrder.length === cards.length
    ? nodeState.cardOrder
    : cards.map((_, idx) => idx);
  if (!Array.isArray(nodeState.cardOrder) || nodeState.cardOrder.length !== cards.length) {
    const shuffled = [...cardOrder];
    for (let i = shuffled.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    nodeState.cardOrder = shuffled;
    nodeState.activeCardIndex = 0;
    nodeState.revealedCard = false;
    window.setNodeInteractionState(node.id, nodeState);
  }
  const order = nodeState.cardOrder || cardOrder;
  const activeCardIndex = Math.min(nodeState.activeCardIndex || 0, order.length - 1);
  const activeIdx = order[activeCardIndex];
  const card = cards[activeIdx];
  const revealed = !!nodeState.revealedCard;
  const easeByCard = nodeState.easeByCard || {};
  const ease = easeByCard[activeIdx] || '';
  const prompt = window.i18nText(card.prompt_i18n, locale, card.prompt_zh_tw || '');
  const answer = window.i18nText(card.answer_i18n, locale, card.answer_zh_tw || '');
  const note = window.i18nText(card.note_i18n, locale, card.note_zh_tw || '');

  return `
    <div class="interaction-panel animate-in">
      <div class="interaction-label">🗂️ Flashcard Review (${activeCardIndex + 1}/${cards.length})</div>
      <div class="summary-box" style="background:#fff; border-radius:12px; padding:16px;">
        <div class="tiny-text muted" style="margin-bottom:6px;">卡片正面</div>
        <div style="font-size:22px; font-weight:700; line-height:1.5;">
          ${window.escapeHtml(card.front_ko || '')}
          ${card.front_ko ? window.renderSpeakButton(card.front_ko) : ''}
        </div>
        ${prompt ? `<div class="muted-text" style="margin-top:8px;">${window.escapeHtml(prompt)}</div>` : ''}
      </div>
      <div class="btn-row" style="margin-top:12px;">
        <button class="btn primary" onclick="toggleFlashcardReveal()">${revealed ? '收起答案' : '翻頁看答案'}</button>
      </div>
      ${revealed ? `
        <div class="summary-box" style="margin-top:12px; border-color:var(--ok-soft); background:var(--ok-soft);">
          <div class="tiny-text muted" style="margin-bottom:6px;">卡片背面</div>
          ${answer ? `<div style="font-weight:700; margin-bottom:6px;">${window.escapeHtml(answer)}</div>` : ''}
          ${card.back_ko ? `<div style="font-size:18px; font-weight:700;">${window.escapeHtml(card.back_ko)} ${window.renderSpeakButton(card.back_ko)}</div>` : ''}
          ${note ? `<div class="tiny-text muted" style="margin-top:8px;">${window.escapeHtml(note)}</div>` : ''}
        </div>
      ` : ''}
      <div style="margin-top:12px;">
        <div class="tiny-text muted" style="margin-bottom:8px;">熟練度</div>
        <div class="btn-group" style="flex-wrap:wrap; gap:8px;">
          ${[
            ['again', 'Again'],
            ['hard', 'Hard'],
            ['good', 'Good'],
            ['easy', 'Easy'],
          ].map(([key, label]) => `
            <button class="btn ${ease === key ? 'success' : ''}" style="font-size:12px; padding:6px 12px;" onclick="rateFlashcard('${key}')">${label}</button>
          `).join('')}
        </div>
      </div>
      <div class="btn-row" style="margin-top:12px;">
        <button class="btn" ${activeCardIndex <= 0 ? 'disabled' : ''} onclick="prevFlashcard()">上一張</button>
        <button class="btn" ${activeCardIndex >= cards.length - 1 ? 'disabled' : ''} onclick="nextFlashcard()">下一張</button>
      </div>
    </div>
  `;
};

window.renderFreeNote = function (node) {
  const nodeState = window.getNodeInteractionState(node.id);
  return `
    <div style="margin-top:40px; border-top:1px solid var(--line); padding-top:20px;">
      <div class="block-title">個人筆記</div>
      <textarea style="min-height:80px; font-size:13px;" placeholder="記錄本節心得或卡關點..." oninput="updateNote(this.value)">${window.escapeHtml(nodeState.note || '')}</textarea>
    </div>
  `;
};

// --- Registry Initialization ---

window.RendererRegistry.registerContent('dialogue', renderDialogue);
window.RendererRegistry.registerContent('pattern_lab', renderPatternLab);
window.RendererRegistry.registerContent('comprehension_check', renderComprehensionCheck);
window.RendererRegistry.registerContent('notice', renderNotice);
window.RendererRegistry.registerContent('message_thread', renderMessageThread);
window.RendererRegistry.registerContent('comparison_card', renderComparison);
window.RendererRegistry.registerContent('pattern_card', renderPatternCard);
window.RendererRegistry.registerContent('grammar_note', renderGrammar);
window.RendererRegistry.registerContent('functional_phrase_pack', renderDictionary);
window.RendererRegistry.registerContent('practice_card', renderPracticeCardHead);
window.RendererRegistry.registerContent('roleplay_prompt', renderRoleplayPrompt);
window.RendererRegistry.registerContent('message_prompt', renderMessagePrompt);
window.RendererRegistry.registerContent('review_card', renderReviewCard);
window.RendererRegistry.registerContent('quiz_item', renderQuizItem);

window.RendererRegistry.registerInteraction('chunk_assembly', renderChunkAssemblyMode);
window.RendererRegistry.registerInteraction('response_builder', renderResponseBuilderMode);
window.RendererRegistry.registerInteraction('frame_fill', renderFrameFillMode);
window.RendererRegistry.registerInteraction('pattern_transform', renderPatternTransformMode);
window.RendererRegistry.registerInteraction('guided', renderGuidedOutputMode);
window.RendererRegistry.registerInteraction('review_retrieval', renderReviewRetrievalMode);
window.RendererRegistry.registerInteraction('flashcard_review', renderFlashcardReviewMode);

// --- Global Interaction Wrappers ---

window.addChunk = (txt) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  if (!s.answers) s.answers = [];
  s.answers.push(txt);
  if (s.feedbackByTaskIndex) {
    const key = s.taskOrder?.[s.activeTaskIndex || 0];
    if (typeof key !== 'undefined') delete s.feedbackByTaskIndex[key];
  }
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
};
window.removeChunk = (idx) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.answers.splice(idx, 1);
  if (s.feedbackByTaskIndex) {
    const key = s.taskOrder?.[s.activeTaskIndex || 0];
    if (typeof key !== 'undefined') delete s.feedbackByTaskIndex[key];
  }
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
};
window.clearAssembly = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.answers = [];
  if (s.feedbackByTaskIndex) {
    const key = s.taskOrder?.[s.activeTaskIndex || 0];
    if (typeof key !== 'undefined') delete s.feedbackByTaskIndex[key];
  }
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
};
window.checkAssembly = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  const tasks = node.payload.tasks || [];
  const order = s.taskOrder || tasks.map((_, idx) => idx);
  const activeTaskIndex = Math.max(0, Math.min(s.activeTaskIndex || 0, tasks.length - 1));
  const task = tasks[order[activeTaskIndex]];
  if (!task) return;
  const answer = (s.answers || []).join(' ').trim();
  const targets = task.target_examples || [];
  const acceptable = task.acceptable_examples || [];
  let kind = 'incorrect';
  let message = `這句不是這題要練的內容。先看主語、名詞和語尾是不是都選對了。`;
  if (targets.includes(answer)) {
    kind = 'best_fit';
    message = `對，這個場合最自然就是這樣說。`;
  } else if (acceptable.includes(answer)) {
    kind = 'acceptable_but_less_natural';
    message = `這句文法上可以，但這個場合更自然的是 ${targets[0] || '目標句'}。`;
  } else if (!answer) {
    message = '先把句子組出來，再檢查。';
  }
  if (!s.feedbackByTaskIndex) s.feedbackByTaskIndex = {};
  s.feedbackByTaskIndex[order[activeTaskIndex]] = { kind, message, answer };
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
};
window.toggleTaskExample = () => {
  const box = document.getElementById('assemblyExample');
  if (!box) return;
  box.style.display = box.style.display === 'none' ? 'block' : 'none';
  if (box.style.display === 'block') window.showToast('已顯示示例');
};
window.nextTask = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  const tasks = node.payload.tasks || [];
  const shuffleArray = (arr) => {
    const next = [...arr];
    for (let i = next.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [next[i], next[j]] = [next[j], next[i]];
    }
    return next;
  };
  const currentIdx = s.activeTaskIndex || 0;
  if (currentIdx >= tasks.length - 1) {
    s.taskOrder = shuffleArray(tasks.map((_, idx) => idx));
    s.chunkOrderByTaskIndex = Object.fromEntries(
      tasks.map((task, idx) => [idx, shuffleArray(task.chunks || [])])
    );
    s.activeTaskIndex = 0;
  } else {
    s.activeTaskIndex = currentIdx + 1;
  }
  s.answers = [];
  if (s.feedbackByTaskIndex) delete s.feedbackByTaskIndex[order[s.activeTaskIndex]];
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
  window.showToast(currentIdx >= tasks.length - 1 ? '已重新洗題' : '載入下一題');
};
window.pickResponse = (idx, choice) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  if (!s.chosenByIndex) s.chosenByIndex = {};
  s.chosenByIndex[idx] = choice;
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
  window.showToast('已更新選擇');
};
window.updateDraft = (val) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  window.setNodeInteractionState(node.id, { draft: val });
};
window.toggleFlashcardReveal = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.revealedCard = !s.revealedCard;
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
};
window.rateFlashcard = (rating) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  const cards = node.payload.cards || [];
  const order = s.cardOrder || cards.map((_, idx) => idx);
  const activeCardIndex = Math.min(s.activeCardIndex || 0, order.length - 1);
  const activeIdx = order[activeCardIndex];
  if (!s.easeByCard) s.easeByCard = {};
  s.easeByCard[activeIdx] = rating;
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
  window.showToast(`已標記 ${rating}`);
};
window.nextFlashcard = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  const cards = node.payload.cards || [];
  s.activeCardIndex = Math.min((s.activeCardIndex || 0) + 1, cards.length - 1);
  s.revealedCard = false;
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
};
window.prevFlashcard = () => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.activeCardIndex = Math.max((s.activeCardIndex || 0) - 1, 0);
  s.revealedCard = false;
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentInteractionOnly();
};
window.updateRetrievalDraft = (idx, val) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.retrievalDrafts = { ...(s.retrievalDrafts || {}), [idx]: val };
  window.setNodeInteractionState(node.id, s);
};
window.toggleRetrievalHint = (idx) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.revealedHints = { ...(s.revealedHints || {}), [idx]: !((s.revealedHints || {})[idx]) };
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
};
window.toggleRetrievalAnswer = (idx) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  const s = window.getNodeInteractionState(node.id);
  s.revealedAnswers = { ...(s.revealedAnswers || {}), [idx]: !((s.revealedAnswers || {})[idx]) };
  window.setNodeInteractionState(node.id, s);
  window.renderCurrentNode();
};
window.updateNote = (val) => {
  const node = window.state.data.sequence[window.state.currentIndex];
  window.setNodeInteractionState(node.id, { note: val });
};
