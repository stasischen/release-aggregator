/**
 * Grammar Renderer Component
 */

(function () {
  function renderGrammar(node) {
    const payload = node.payload || {};
    const locale = window.currentLocale();

    // 1. Determine Sections (Priority 1: payload.sections, Priority 2: top-level points)
    let sections = [];
    let isLegacy = false;
    let malformedReason = null;

    if (payload.sections) {
      if (Array.isArray(payload.sections)) {
        sections = payload.sections;
      } else {
        malformedReason = "payload.sections MUST be an array.";
      }
    } else if (payload.points_i18n || payload.points) {
      const pts = payload.points_i18n || payload.points;
      if (Array.isArray(pts)) {
        sections = [{
          title_i18n: { zh_tw: window.getLabel('key_points'), en: window.getLabel('key_points') },
          points_i18n: pts
        }];
      } else {
        malformedReason = "Legacy points MUST be an array.";
      }
    }

    // 2. Fail-Soft Detection
    if (sections.length === 0) {
      if (malformedReason) {
        return window.renderDataInspection(payload, malformedReason);
      }
      
      const hasOtherKeys = Object.keys(payload).some(k => !['sections', 'points', 'points_i18n', 'notice_i18n', 'what_to_notice_i18n'].includes(k));
      if (hasOtherKeys) {
        // Unknown payload but not explicitly marked as malformed array yet
        return window.renderDataInspection(payload, 'Unrecognized Grammar Payload Structure');
      }
      // Valid but empty
      return `
        <div class="grammar-container animate-in">
          ${window.renderNotice(payload)}
          ${window.renderEmptyState(window.getLabel('no_grammar'))}
        </div>
      `;
    }

    // 3. Render Sections
    const html = sections.map(s => {
      const title = window.i18nText(s.title_i18n, locale, window.getLabel('grammar_points'));
      const explanationMd = window.i18nText(s.explanation_md_i18n, locale, s.explanation_md || '');
      const points = window.LessonAdapter.resolveArray(s.points_i18n || s.points || []);

      let sectionContent = '';
      
      // Coexistence: Render MD first, then points
      if (explanationMd) {
        sectionContent += `<div class="md-block">${window.markdownToHtmlLite(explanationMd)}</div>`;
      }
      
      if (points.length > 0) {
        sectionContent += `
          <ul class="grammar-point-list">
            ${points.map(p => `
              <li>${window.applyInlineMarkdown(window.i18nText(p, locale, p))}</li>
            `).join('')}
          </ul>
        `;
      }

      return `
        <details open>
          <summary>${window.escapeHtml(title)}</summary>
          <div class="grammar-body">
            ${sectionContent || `<div class="muted-text tiny-text">${window.getLabel('empty_content')}</div>`}
          </div>
        </details>
      `;
    }).join('');

    // 4. Examples (Unified via Adapter-resolved property)
    const examplesHtml = window.renderUnifiedExampleSection(payload.resolved_examples);

    return `
      <div class="grammar-container animate-in">
        ${window.renderNotice(payload)}
        <div class="content-block">
          <div class="block-title">${window.getLabel('grammar_explanation')}</div>
          <div class="grammar-accordion">
            ${html}
          </div>
        </div>
        ${examplesHtml}
      </div>
    `;
  }

  window.RendererRegistry.registerContent('grammar_note', renderGrammar);
  window.RendererRegistry.registerContent('grammar_summary', renderGrammar);
})();
