/**
 * Vocab Renderer Component
 */
(function () {
  function renderVocab(node) {
    const payload = node.payload || {};
    const locale = window.currentLocale();
    
    // 1. Resolve Items (Priority 1: payload.items, Priority 2: payload.sections)
    let sections = [];
    if (payload.sections && Array.isArray(payload.sections)) {
      sections = payload.sections;
    } else if (payload.items && Array.isArray(payload.items)) {
      sections = [{
        title_i18n: { zh_tw: window.getLabel('vocab_list'), en: window.getLabel('vocab_list') },
        items: payload.items
      }];
    }

    // 2. Fail-Soft Detection
    if (sections.length === 0) {
        return `
          <div class="vocab-container animate-in">
            ${window.renderNotice(payload)}
            ${window.renderEmptyState(window.getLabel('no_vocab'))}
          </div>
        `;
    }

    // 3. Render Sections & Items
    const html = sections.map(s => {
      const title = window.i18nText(s.title_i18n, locale, window.getLabel('vocab_list'));
      const items = window.LessonAdapter.resolveArray(s.items || []);
      const itemGlossByKo = s.item_gloss_by_ko || payload.item_gloss_by_ko || {};

      if (items.length === 0) return '';

      return `
        <div class="vocab-section">
          <div class="section-subtitle">${window.escapeHtml(title)}</div>
          <div class="vocab-list">
            ${items.map(item => {
              // item can be a string or an object
              let target = '';
              let gloss = '';
              let exampleKo = '';
              let exampleZh = '';

              if (typeof item === 'string') {
                target = item;
                gloss = itemGlossByKo[item] || '';
              } else {
                target = item.ko || item.target || '';
                gloss = window.i18nText(item.explain_i18n, locale, item.gloss || item.translation || '');
                exampleKo = item.example_ko || '';
                exampleZh = window.i18nText(item.example_i18n, locale, '');
              }

              return `
                <div class="vocab-item">
                  <div class="vocab-row">
                    <span class="vocab-target" onclick="window.speakKo('${target.replace(/'/g, "\\'")}')">${window.escapeHtml(target)}</span>
                    <span class="vocab-gloss">${window.escapeHtml(gloss)}</span>
                  </div>
                  ${exampleKo ? `
                    <div class="vocab-example">
                      <div class="ko-ex">${window.escapeHtml(exampleKo)}</div>
                      <div class="translation-ex muted-text tiny-text">${window.escapeHtml(exampleZh)}</div>
                    </div>
                  ` : ''}
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="vocab-container animate-in">
        ${window.renderNotice(payload)}
        <div class="content-block">
          <div class="block-title">${window.getLabel('vocab_and_phrases')}</div>
          ${html}
        </div>
      </div>
    `;
  }

  window.RendererRegistry.registerContent('vocab_summary', renderVocab);
  window.RendererRegistry.registerContent('vocab_note', renderVocab);
  window.RendererRegistry.registerContent('functional_phrase_pack', renderVocab);
})();
