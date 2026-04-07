/**
 * Usage Renderer Component
 */
(function () {
  function renderUsage(node) {
    const payload = node.payload || {};
    const locale = window.currentLocale();

    // Usage often relies on notice and support modules.
    const noticeHtml = window.renderNotice(payload);
    const supportHtml = window.renderLessonSupportModule(payload.support_module || payload.supplementary_info);
    
    // If we have an explanation or examples directly in the payload
    const explanation = window.i18nText(payload.explanation_i18n, locale, payload.explanation_zh_tw || '');
    const examples = window.LessonAdapter.resolveArray(payload.examples || []);

    const hasContent = noticeHtml || supportHtml || explanation || examples.length > 0;

    if (!hasContent) {
      return `
        <div class="usage-container animate-in">
          ${window.renderEmptyState('本節點目前無詳細用法說明。')}
        </div>
      `;
    }

    let exampleHtml = '';
    if (examples.length > 0) {
      exampleHtml = `
        <div class="content-block animate-in" style="margin-top:16px;">
          <div class="block-title">用法示例 (Examples)</div>
          <div class="usage-examples">
            ${examples.map(ex => `
              <div class="usage-ex-item" onclick="window.speakKo('${(ex.text || ex.ko || '').replace(/'/g, "\\'")}')">
                <div class="ko-ex">${window.escapeHtml(ex.text || ex.ko || '')}</div>
                <div class="zh-ex muted-text tiny-text">${window.escapeHtml(window.i18nText(ex.zh_tw_i18n, locale, ex.zh_tw || ''))}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    return `
      <div class="usage-container animate-in">
        ${noticeHtml}
        ${explanation ? `<div class="content-block"><div class="md-block">${window.markdownToHtmlLite(explanation)}</div></div>` : ''}
        ${supportHtml}
        ${exampleHtml}
      </div>
    `;
  }

  window.RendererRegistry.registerContent('usage', renderUsage);
})();
