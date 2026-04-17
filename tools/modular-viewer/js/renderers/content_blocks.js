/**
 * Shared Content Blocks
 * Reusable UI fragments used by content renderers.
 */

window.renderEmptyState = function (message = 'No additional details available.') {
  return `
    <div class="empty-state animate-in">
      <div class="icon" style="font-size:24px; margin-bottom:8px;">☕</div>
      <div class="muted-text">${window.escapeHtml(message)}</div>
      <p class="tiny-text" style="color:var(--muted); margin-top:4px;">本節點內容較為大綱式，請配合課堂練習進行。</p>
    </div>
  `;
};

window.renderUnifiedExampleSection = function (examples) {
  if (!examples || examples.length === 0) return '';
  
  const isCanonical = examples[0]?.is_canonical;
  const title = '例句';
  const badgeClass = isCanonical ? 'tag-canonical' : 'tag-transitional';
  const badgeText = isCanonical ? 'Canonical' : 'Transitional';

  return `
    <div class="example-section animate-in" style="margin-top:24px;">
      <div class="section-subtitle" style="display:flex; align-items:center; gap:8px;">
        ${title}
        <span class="tiny-tag ${badgeClass}">${badgeText}</span>
      </div>
      <div class="example-grid">
        ${examples.map(ex => {
          const fallbackKo = window.escapeJsSingle(ex.ko);
          return `
            <div class="example-card">
              <div class="example-header">
                <div class="example-ko">${window.escapeHtml(ex.ko)}</div>
                <button type="button" class="audio-btn" data-text="${fallbackKo}">
                  <span class="icon">🔊</span>
                </button>
              </div>
              <div class="example-zh">${window.escapeHtml(ex.translation || '')}</div>
            </div>
          `;
        }).join('')}
      </div>
    </div>
  `;
};

window.renderNotice = function (payload) {
  if (!payload) return '';
  const finalItems = (payload.what_to_notice_i18n || []).map(v => window.i18nText(v)).filter(Boolean);
  if (finalItems.length === 0) return '';

  return `
    <div class="notice-box animate-in">
      <div class="notice-title">💡 重點觀察 (Notice)</div>
      <ul>
        ${finalItems.map(item => `<li>${window.escapeHtml(item)}</li>`).join('')}
      </ul>
    </div>
  `;
};

window.renderLessonSupportModule = function (module) {
  if (!module) return '';
  const title = window.i18nText(module.title_i18n, window.currentLocale(), '應援小提醒');
  const why = window.i18nText(module.why_here_i18n, window.currentLocale(), '');

  return `
    <div class="support-module animate-in">
      <div class="support-header">📚 應援：${window.escapeHtml(title)}</div>
      <div class="support-body">
        <div class="why-text">${window.markdownToHtmlLite(why)}</div>
        <div class="support-items">
          ${(module.items || []).map(item => `
            <div class="support-item">
              <span class="target">${window.escapeHtml(item.target || item.ko || '')}</span>
              <span class="explain">${window.escapeHtml(window.i18nText(item.explain_i18n, window.currentLocale(), ''))}</span>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
};
