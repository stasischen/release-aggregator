/**
 * Grammar Renderer Component
 */

(function () {
    function renderGrammar(node) {
        const payload = node.payload || {};
        const body = document.getElementById('detailBody');
        const locale = window.currentLocale();

        // Support both 'grammar_note' and 'grammar_summary'
        const sections = payload.sections || (payload.points ? [{ title_i18n: { zh_tw: '重點內容' }, points_i18n: payload.points }] : []);

        const html = sections.map(s => `
      <details open>
        <summary>${window.escapeHtml(window.i18nText(s.title_i18n, locale, s.title_zh_tw || '文法重點'))}</summary>
        <div class="grammar-body">
          ${window.i18nText(s.explanation_md_i18n, locale, s.explanation_md || '')
                ? `<div class="md-block">${window.markdownToHtmlLite(window.i18nText(s.explanation_md_i18n, locale, s.explanation_md || ''))}</div>`
                : `
              <ul class="grammar-point-list">
                ${(s.points_i18n || s.points_zh_tw || []).map(p => `
                  <li>${window.applyInlineMarkdown(window.i18nText(p, locale, p))}</li>
                `).join('')}
              </ul>
            `
            }
        </div>
      </details>
    `).join('');

        body.innerHTML = `
      <div class="grammar-container animate-in">
        ${window.renderNotice(payload)}
        <div class="content-block">
          <div class="block-title">文法解說</div>
          <div class="grammar-accordion">
            ${html || '<div class="empty-state">無資料</div>'}
          </div>
        </div>
      </div>
    `;
    }

    window.RendererRegistry.registerContent('grammar_note', renderGrammar);
    window.RendererRegistry.registerContent('grammar_summary', renderGrammar);
})();
