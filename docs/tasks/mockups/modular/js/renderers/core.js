/**
 * Lingourmet Renderer Registry & Core Helpers
 */

window.RendererRegistry = {
  renderers: {},
  register(contentForm, interactionMode, fn) {
    const key = `${contentForm}:${interactionMode}`;
    this.renderers[key] = fn;
  },
  registerContent(contentForm, fn) {
    this.renderers[contentForm] = fn;
  },
  registerInteraction(mode, fn) {
    this.renderers[mode] = fn;
  },
  dispatch(node) {
    const contentForm = node.content_form || 'unknown';
    const outputMode = node.output_mode || 'none';
    const key = `${contentForm}:${outputMode}`;

    let contentHtml = '';
    let interactionHtml = '';

    if (this.renderers[key]) {
      contentHtml = this.renderers[key](node) || '';
    } else if (this.renderers[contentForm]) {
      contentHtml = this.renderers[contentForm](node) || '';
    } else {
      contentHtml = this.renderFallback(node);
    }

    // Interaction dispatch (if separate)
    if (this.renderers[outputMode]) {
      interactionHtml = this.renderers[outputMode](node) || '';
    }

    return { contentHtml, interactionHtml };
  },
  renderFallback(node) {
    return `
      <div class="empty-state animate-in">
        <div class="icon">❓</div>
        <h3>未知的內容類型: ${node.content_form}</h3>
        <p class="muted-text">請檢查渲染器註冊或資料格式。</p>
        <pre style="text-align:left; background:#f0f0f0; padding:12px; font-size:10px;">${JSON.stringify(node.payload, null, 2)}</pre>
      </div>
    `;
  }
};

// --- Shell Renderers ---

window.renderDetailHeader = function (node) {
  const locale = window.currentLocale();
  const el = document.getElementById('detailHeader');
  if (!el) return;
  const stage = window.nodeStageLabel(node.id) || '';
  const skillFocus = window.nodeSkillFocusText(node);

  el.innerHTML = `
    <div class="detail-header-card animate-in">
      <div class="tiny-text muted">${window.escapeHtml(stage || node.learning_role || 'node')}</div>
      <h2 style="margin:4px 0 8px;">${window.escapeHtml(window.nodeTitleText(node, locale))}</h2>
      <div class="meta-tags">
        <span class="tag">${window.escapeHtml(node.content_form || 'unknown')}</span>
        <span class="tag">${window.escapeHtml(node.learning_role || 'learning')}</span>
        <span class="tag">${window.escapeHtml(skillFocus)}</span>
      </div>
    </div>
  `;
};

window.renderDetailSummary = function (node) {
  const locale = window.currentLocale();
  const el = document.getElementById('detailSummary');
  if (!el) return;
  const summary = window.nodeSummaryText(node, locale);
  const expected = window.nodeExpectedText(node, locale);
  el.innerHTML = `
    <div class="summary-grid animate-in" style="margin-bottom:12px;">
      <div class="summary-box">
        <span class="label">本節目標</span>
        ${window.escapeHtml(summary)}
      </div>
      <div class="summary-box">
        <span class="label">預期輸出</span>
        ${window.escapeHtml(expected)}
      </div>
    </div>
  `;
};

window.renderFreeNote = function (node) {
  return `
      <div class="free-note-box animate-in">
        <textarea placeholder="隨手筆記 (Free Note)..."></textarea>
      </div>
    `;
};


// --- Markdown & Text Processing ---

window.applyInlineMarkdown = function (text) {
  return String(text || '')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>');
};

window.markdownToHtmlLite = function (md) {
  const src = String(md || '').replace(/\r\n/g, '\n');
  const lines = src.split('\n');
  const out = [];
  let i = 0;

  const isTableSeparator = (line) => /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line);
  const isTableRow = (line) => line.includes('|');

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();
    if (!trimmed) { i++; continue; }

    if (i + 1 < lines.length && isTableRow(lines[i]) && isTableSeparator(lines[i + 1])) {
      const headerCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
      i += 2;
      const bodyRows = [];
      while (i < lines.length && isTableRow(lines[i]) && lines[i].trim()) {
        const rowCells = lines[i].split('|').map(c => c.trim()).filter(Boolean);
        if (rowCells.length) bodyRows.push(rowCells);
        i++;
      }
      out.push(`
        <div class="md-table-wrap">
          <table class="md-table">
            <thead><tr>${headerCells.map(c => `<th>${window.applyInlineMarkdown(c)}</th>`).join('')}</tr></thead>
            <tbody>${bodyRows.map(r => `<tr>${r.map(c => `<td>${window.applyInlineMarkdown(c)}</td>`).join('')}</tr>`).join('')}</tbody>
          </table>
        </div>
      `);
      continue;
    }

    if (trimmed.startsWith('- ')) {
      const items = [];
      while (i < lines.length && lines[i].trim().startsWith('- ')) {
        items.push(lines[i].trim().slice(2));
        i++;
      }
      out.push(`<ul class="grammar-point-list">${items.map(p => `<li>${window.applyInlineMarkdown(p)}</li>`).join('')}</ul>`);
      continue;
    }

    out.push(`<p class="md-paragraph">${window.applyInlineMarkdown(trimmed)}</p>`);
    i++;
  }
  return out.join('');
};

// --- Reusable Content Blocks ---

window.renderNotice = function (payload) {
  if (!payload) return '';
  const items = (payload.what_to_notice_i18n || []).map(v => window.i18nText(v)).filter(Boolean);
  const legacyItems = payload.notice_items_zh_tw || [];
  const finalItems = items.length > 0 ? items : legacyItems;

  if (finalItems.length === 0 && !payload.notice_zh_tw) return '';

  return `
    <div class="notice-box animate-in">
      <div class="notice-title">💡 重點觀察 (Notice)</div>
      <ul>
        ${finalItems.map(item => `<li>${window.escapeHtml(item)}</li>`).join('')}
        ${payload.notice_zh_tw ? `<li>${window.escapeHtml(payload.notice_zh_tw)}</li>` : ''}
      </ul>
    </div>
  `;
};

window.renderLessonSupportModule = function (module) {
  if (!module) return '';
  const title = window.i18nText(module.title_i18n, window.currentLocale(), module.title_zh_tw || '應援小提醒');
  const why = window.i18nText(module.why_here_i18n, window.currentLocale(), module.why_here_zh_tw || '');

  return `
    <div class="support-module animate-in">
      <div class="support-header">📚 應援：${window.escapeHtml(title)}</div>
      <div class="support-body">
        <div class="why-text">${window.markdownToHtmlLite(why)}</div>
        <div class="support-items">
          ${(module.items || []).map(item => `
            <div class="support-item">
              <span class="target">${window.escapeHtml(item.target || item.ko || '')}</span>
              <span class="explain">${window.escapeHtml(window.i18nText(item.explain_i18n, window.currentLocale(), item.explain_zh_tw || ''))}</span>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
};

// --- Global UI Context Helpers ---

window.currentLocale = () => window.state.progress.prefs.teachingLocale || 'zh_tw';
window.currentTeachingLocale = window.currentLocale;
window.showBilingual = () => window.state.progress.prefs.showBilingual !== false;

// --- Legacy Helper Mapping ---

window.nodeTitleText = (node, locale) => node.displayTitle || window.LessonAdapter.resolveText(node && node.title_i18n, locale, (node && node.title_zh_tw) || window.LessonAdapter.getFallbackNodeTitle(node));
window.nodeSummaryText = (node, locale) => node.displaySummary || window.LessonAdapter.resolveText(node && node.summary_i18n, locale, (node && node.summary_zh_tw) || '先看這一節的內容。');
window.nodeExpectedText = (node, locale) => node.displayExpected || window.LessonAdapter.resolveText(node && node.expected_output_i18n, locale, (node && node.expected_output_zh_tw) || '先理解這一節的重點。');

window.nodeSkillFocusText = function (node) {
  if (node.skill_focus && node.skill_focus.length > 0) return node.skill_focus.join(' · ');
  const id = node.id || '';
  if (id.includes('-L')) return 'listening · reading';
  if (id.includes('-G')) return 'grammar · reading';
  if (id.includes('-P')) return 'speaking · output';
  return 'learning';
};

window.nodeStageLabel = function (nodeId) {
  const match = String(nodeId || '').match(/-(L1|L2|L3|G1|G2|P1|P2|P5|R1)$/);
  return match ? match[1] : '';
};
