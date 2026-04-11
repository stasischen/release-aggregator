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
    
    // If we have an explanation directly in the payload
    const explanation = window.i18nText(payload.explanation_md_i18n || payload.explanation_i18n, locale, payload.explanation_md_zh_tw || payload.explanation_zh_tw || '');
    const resolvedExamples = payload.resolved_examples || [];

    const hasContent = noticeHtml || supportHtml || explanation || resolvedExamples.length > 0;

    if (!hasContent) {
      return `
        <div class="usage-container animate-in">
          ${window.renderEmptyState('本節點目前無詳細用法說明。')}
        </div>
      `;
    }

    const exampleHtml = window.renderUnifiedExampleSection(resolvedExamples);

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
